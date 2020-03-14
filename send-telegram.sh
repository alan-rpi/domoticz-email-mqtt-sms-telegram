#!/bin/bash
# This script presumes you have stored the python script within the same folder as this sh. script.
# For a Docker implementation this is normally in /config/ which is mapped to your folder outside of Docker.
#
# Get the path to the scripts. 
PATH="`dirname \"$0\"`"
if [[ $PATH == "." ]]; then
    myPath=""
else
    myPath="${PATH}/"
fi
${myPath}send-telegram.py "$@"