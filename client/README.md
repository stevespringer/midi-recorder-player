# Windows Client

These autohotkey and python scripts allow the user to access midi recordings by calling the TCP server.

Right-clicking the system tray icon loads recording sessions from the previous few days and populates a context menu. When you click on a session, the midi files are requested and deserialised, and the running instance of Reaper is triggered execute the python reascript, which loads each file into a new track.

## Why not do this all through Reaper?

The python implementation is pretty limited, and I didn't want to learn the other reascript languages.

## Why use a csv file as an intermediary for the menu contents?

Autohotkey doesn't give you a simple build in way to read the standard out of a Run command (AFAIK).

## Why the shell script to "generate" the python reascript?

I needed to pass the midi folder path but python reascript doesn't know what the executing script path is to read the config file.

## Why use an ini file for the config?

Native support in both AHK and Python.

## Why is the Reascript invoked via a shortcut key (F1)?

I couldn't find another way to programatically trigger a python reascript, or to add it to the reaper menu. Therefore this will only ever work with one reascript (as I have bound F1 as the shortcut key to the Reaper action "Run last ReaScript")
