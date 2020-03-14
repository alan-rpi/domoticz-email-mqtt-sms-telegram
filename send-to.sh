#!/bin/bash
# A script to call one or more of send-email, send-sms, send-mqtt, send-telegram python functions
# This reduces the number of Call Script statements in a Blockly rule
#
# Parmaters are: "<list of function IDs to call>" "<message>" "<subject>" "<topic>" "<Y/N datetimestamp option>"
#       where function IDs list contains E for Email, S for SMS, M for MQTT and T for Telegram
#
# The functions are then called with the following parameters:
#   Email:      "<message>" "<subject>" ""  "<Y/N datetimestamp option>"
#   SMS:        "<subject> <message>" ""  "" ""  "<Y/N datetimestamp option">   - i.e. subject & message are combined
#   MQTT:       "<topic>" "<subject> <message>" "Y/N datetimestamp option"  - i.e. value=subject & message combined
#   Telegram:   "<subject> <message>" "" "" ""   "<Y/N timestamp option">   - i.e. subject & message are combined
#
# If any arguement is omitted then the defaults defined in the indivual script's yml files apply.
#       e.g. default subject in Email yml file is "HA Alert"
#            Blockly script is: send-to.sh with "E" "my message" "my subject"
#            then an Email is sent with the subject "my subject" and the body of "my message" 
# As when calling the .sh scripts directly, you can use the "+" to prefix the default value.
#
# Set the STOP supression ID list to stop a particular script being called.
#       E.g. to stop expensive SMS messages during testing set STOP = "S".
#       Remember to unset for production! 
#
# This Bash .sh script should be in the same folder as the send-xxxx.py scripts.
#
STOP="S"

# Get the path to the scripts. 
PATH="`dirname \"$0\"`"
if [[ $PATH == "." ]]; then
    myPath=""
else
    myPath="${PATH}/"
fi
#echo $# $0 $1 $2 $3 $4 $5
#echo $PATH  ${myPath}

sendTo="$1"
sendTo=${sendTo^^}    # covert to upper case

# capture arguement or set to null if does not exist
if [[ $# -ge 2 ]]; then
    message="$2"
else
    message=""
fi
if [[ $# -ge 3 ]]; then
    subject="$3"
else
    subject=""
fi
if [[ $# -ge 4 ]]; then
    topic="$4"
else
    topic=""
fi
if [[ $# -ge 5 ]]; then
    datetimestamp="$5"
else
    datetimestamp=""
fi

if [[ "$STOP" != "" ]]; then
    echo Warning STOP ID list of $STOP will suppress some messages.
fi

# Send to requested methods unless in STOP list
if [[ "$sendTo" == *"E"* && "$STOP" != *"E"* ]]; then
    echo Calling ${myPath}send-email "$message" "$subject" "" "$datetimestamp" 
    ${myPath}send-email.py "$message" "$subject" "" "$datetimestamp" 
fi
if [[  "$sendTo" == *"S"* && "$STOP" != *"S"* ]]; then
    echo Calling send-sms "$subject $message" "" "" "" "$datetimestamp"
    ${myPath}send-sms.py "$subject $message" "" "" "" "$datetimestamp"
fi
if [[  "$sendTo" == *"M"* && "$STOP" != *"M"* ]]; then 
    echo Calling send-mqtt  "$topic" "$subject $message" "$datetimestamp"
    ${myPath}send-mqtt.py "$topic" "$subject $message" "$datetimestamp" 
fi
if [[  "$sendTo" == *"T"* && "$STOP" != *"T"* ]]; then
    echo Calling send-telegram  "$subject $message" "" "" "" "$datetimestamp"
    ${myPath}send-telegram.py "$subject $message" "" "" "" "$datetimestamp"
fi
