# Always on MIDI Recorder and file server

This consists of:

 - A bash script (scheduled on boot via systemd unit file) to capture any midi output from a specific device, saving the recordings to midi files at periods of silence.
 - A python script to serve the midi recordings over TCP, allowing clients to list recordings and download sessions (defined as a set of recordings made within a close period of time).

## MIDI Recorder

This script functions similarly to, and is inspired by, the "Brainstorm" utility in [Div's MIDI Utilities](http://www.sreal.com/~div/midi-utilities/). The differences are:

 - It's a bash script, rather than a compilec C program.
 - It interacts with MIDI devices via the utilities present in ALSA rather than rtmidi.
 - It can be started when the MIDI device is off and will listen to the MIDI Announce channel to check for device connection and automatically start recording.

## File Server

The client folder of this repo accesses MIDI recordings through this script. This enables the MIDI Recorder to run "headless" on a linux device connected to mu MIDI input, and my laptop to connect via TCP when I want to access the recordings that have been saved.

Requested MIDI files are base-64 encoded and sent back to the client, which can decode the files and recreate them on the local computer.
