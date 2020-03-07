#!/bin/bash
# Set the path to the script. See the README for using a directory within the Domoticz container. 
# The default /config/ presumes you have stored the python script within the mapped directory.
# The default below presumes the python script has been renamed from send-email-template.py
python3 /config/send-email.py "$@"