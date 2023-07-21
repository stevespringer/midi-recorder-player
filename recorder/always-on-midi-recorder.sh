#!/bin/bash

TZ='BST0GMT,M3.2.0/2:00:00,M11.1.0/2:00:00'; export TZ

while true
do

	pipe=$(mktemp -u) || exit
	mkfifo -m 600 -- "$pipe" || exit

	if aseqdump -l | grep Clavinova >/dev/null ; then
		
		echo "Clavinova found, recording..."

		filename="/var/local/midirecordings/$(date +%Y%m%d%H%M%S).mid"
		arecordmidi -p Clavinova $filename &
		recordingpid=$!

		aseqdump -p 0:1,Clavinova > "$pipe" &
                pid=$!

		result=$(awk '{
    if (/controller 67, value 127/) {print something_happened ? "save" : "replay"; exit 0;}
    if (/Port exit/) {print "disconnected"; exit 0;}
    if (/Note on/) something_happened = 1;
    if (/Active Sensing/) {
        if ($0 == prev_line) {
            count++;
	    if (count > 50 && something_happened) {
          	print "silence";
		exit 0;
    	    }
        }
    } 
    else {
        count = 1;
    }
    prev_line = $0;
}' < "$pipe")

		echo "Saving recording"
                kill -INT $pid $recordingpid

#		if [ $result == "replay" ]; then
#
#		    echo "playing"
#		    rm -f $filename
		    
#		    ls /var/local/midirecordings/*.mid -td | head -1 | xargs ./midi-utilities/bin/playsmf --out 1

#		fi

	else

		echo "Clavinova not found, listening..."

		aseqdump -p 0:1 > "$pipe" &
		pid=$!

		grep -m 1 -E 'Port start\s*20\:0' "$pipe"
		kill -INT $pid
		
	fi

	rm -f -- "$pipe"

done
