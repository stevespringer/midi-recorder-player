#!/bin/bash

source settings.conf

announce_channel="0:1"
pipe="midipipe"

if [ ! -p "$pipe" ]; then
    mkfifo -m 600 -- "$pipe" || exit
fi

while true
do

	if aseqdump -l | grep $MidiDevice >/dev/null ; then
		
		echo "$MidiDevice found, recording..."

		filename="$RecordingsFolder/$(date +%Y%m%d%H%M%S).mid"
		arecordmidi -p $MidiDevice $filename &
		recordingpid=$!

		aseqdump -p $announce_channel,$MidiDevice > "$pipe" &
                pid=$!

		result=$(awk -v output='cancel' '{
    if (/controller 67, value 127/) {exit}
    if (/Port exit/) {exit}
    if (/STOP/) {output = output "replay"; exit;}	    
    if (/Note on/) output = "save";
    if (/Active Sensing/) {
        if ($0 == prev_line) {
            count++;
	    if (count > 50 && output == "save") {
		exit;
    	    }
        }
    } 
    else {
        count = 1;
    }
    prev_line = $0;
  }
  END {
    print output;
  }' < "$pipe")

		echo "Saving recording $filename $result"
                kill -INT $pid $recordingpid
		if [[ $result == cancel* ]]; then
		    echo "No notes played, removing recording"
		    rm -f $filename
		fi


                if [[ $result == *replay ]]; then


		   playfilename=$(ls /var/local/midirecordings/*.mid -td | head -1)
                   echo "playing $playfilename"

		   aplaymidi -p $MidiDevice $playfilename &

               fi

	else

		echo "$MidiDevice not found, listening..."

		aseqdump -p $announce_channel > "$pipe" &
		pid=$!

		grep -m 1 -E 'Port start' "$pipe"
		kill -INT $pid
		
	fi

#	rm -f -- "$pipe"

done
