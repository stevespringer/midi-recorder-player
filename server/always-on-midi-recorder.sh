#!/bin/bash

source settings.conf

while true
do

	pipe=$(mktemp -u) || exit
	mkfifo -m 600 -- "$pipe" || exit

	if aseqdump -l | grep $MidiDevice >/dev/null ; then
		
		echo "$MidiDevice found, recording..."

		filename="$RecordingsFolder/$(date +%Y%m%d%H%M%S).mid"
		arecordmidi -p $MidiDevice $filename &
		recordingpid=$!

		aseqdump -p 0:1,$MidiDevice > "$pipe" &
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

		echo "$MidiDevice not found, listening..."

		aseqdump -p 0:1 > "$pipe" &
		pid=$!

		grep -m 1 -E 'Port start\s*20\:0' "$pipe"
		kill -INT $pid
		
	fi

	rm -f -- "$pipe"

done
