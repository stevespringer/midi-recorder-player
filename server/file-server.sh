#!/bin/bash
source settings.conf
python3 ./file-server.py $RecordingsFolder $ServerPort $MidiDevice
