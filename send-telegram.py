#!/usr/bin/python3
#
# Function to send a Telegram notification. To be called from Domoticz rule. 
#
# Blochly Usage:    Start Script: <optional path to script>/send-telegram.sh  
#                   with parameter(s): "<message text>" "<chat ID>" "<parse option>" "<Y/N silent option>"
#                                      "<Y/N timestamp option"> 
#                                       - all arguements are optional and then defaults will apply
#                                       - provide null "" if subsequent arguements
#                   
# Argurements
# 1. message text   - sent as a single message up to 4,096 characters.
#                     The message text can include Telegram markup or html markup but this has not been tested.
#                     You  can send "+text" to append text to default message
#       Examples:   "My message"    =>  "My message"
#                   "" or omitted   =>  "DefaultMessage"
#                   "+extra text"   =>  "DefaultMessage extra text"
# 2. chat ID        - ID of the recipient
#       Examples:  "1234567890"    =>  "1234567890"
#                  "" or omitted   =>  "DefaultChatID"
# 3. parse         - indicates if the message text contains Telegram Markdown or html formatting or neither (plain text)
#       Examples:   "My important message" and "plain"  =>  the message is sent as written
#                   "My \\*important message" and "markdown"   =>  the word 'important' is bold. Note the \\ escapes
#                   "My <b>important</b> message" and "html"   =>  the word 'important' is bold
#                   "" or omitted   =>  "DefaultMarkUp"      - default is plain text
#                   This option has had limited testing. Markdown is V2.
#                   See https://core.telegram.org/bots/api#formatting-options
# 4. silent         - set to Y so that the recipient will receive the notification with no sound.
#       Examples:   "Y"  =>  no sound on receipt
#                   "" or omitted =>  "DefaultSilentValue"
# 5. datetimestamp - set to Y if the message is to be appended with a date and time stamp
#                   Format is according to the DATETIMEFORMAT setting
#       Examples when Y: and DATETIMEFORMAT= " at %Y-%m-%d %H:%M:%S"
#                   "My message text"   =>  "My message text at 2020-03-10 13:12:45"
#
# Future possible enhancements to include error handling, logging and other Telegram parameters.
#
# Version 1   
# AEC 2020-03-13
# License: GNU General Public License v3.0
#
# User setting are defined in the send-telegram-config.yml file

# script based on example from https://api.thesmsworks.co.uk/docs/api-reference.html#operation/sendMessage
from __future__ import print_function
import http.client
import json
import time
from pprint import pprint
import sys
import os
from datetime import datetime
import yaml         # apt-get install python-yaml


# get configuration settings
with open(os.path.join(sys.path[0], "send-telegram.yml"), 'r') as configfile:
    config = yaml.safe_load(configfile)

HOST = config["HOST"]
URL = config["URL"]
API_KEY = config["API_KEY"]
MESSAGE = config["MESSAGE"]
CHAT_ID = config["CHAT_ID"]
PARSE = config["PARSE"]
SILENT = config["SILENT"]
DATETIMESTAMP = config["DATETIMESTAMP"]
DATETIMEFORMAT = config["DATETIMEFORMAT"]

class sendtelegram:
    def __init__(self):
        pass

    def send(self, arguements): 

        # message is an optional 1st user arguement
        if len(arguements) >= 2:
            message = arguements[1]
            if message != "":       # not null
                # if 1st character is a + then append to the default MESSAGE
                if message[0:1] == "+":
                    message = MESSAGE + " " + message[1:]
                else:
                    message = arguements[1]
            else:
                message = MESSAGE
        else:
            message = MESSAGE

        # chatID is an optional 2nd parameter
        if len(arguements) >= 3:
            if arguements[2] != "":       # not null
                chat_ID = arguements[2]
            else:
                chat_ID = CHAT_ID
        else:
            chat_ID = CHAT_ID

        # parse is an optional 3rd parameter
        if len(arguements) >= 4:
            if arguements[3] != "":       # not null
                parse = arguements[3].upper()
            else:
                parse = PARSE.upper()
        else:
            parse = PARSE.upper()
        if parse == "MARKDOWN":
            parse = "MarkdownV2"
        elif parse == "HTML":
            parse = "HTML"
        else:
            parse = ""

        # silent is an optional 4th user arguement
        if len(arguements) >= 5:
            if arguements[4].upper() == "Y":
                silent = 1
            else:
                silent = 0
        else:
            if SILENT.upper() == "Y":
                silent = 1
            else:
                silent = 0
        silentStr = str(silent).replace("1", "Y").replace("0", "N")

        # datetimestamp is an optional 5th user arguement 
        if len(arguements) >= 6:
            if arguements[5].upper() == "Y":   
                datetimestamp = "Y" 
            else:
                datetimestamp = "N" 
        else:
            datetimestamp = DATETIMESTAMP.upper()
        # apply datetimestamp option, either default or message override option
        if datetimestamp == "Y":
            now = datetime.now()
            message = message + now.strftime(DATETIMEFORMAT)

        # create the https request
        conn = http.client.HTTPSConnection(HOST)
        headers = {'Content-type': 'application/json' }
        
        # build the Telegram message
        payload = {'chat_id': CHAT_ID, 'parse_mode': parse, 'disable_notification' : silent, 'text': message }
        json_data = json.dumps(payload)
        
        # send the message
        conn.request('POST', URL + API_KEY + '/sendMessage', json_data, headers)
        
        # get the response
        response = conn.getresponse()
        responseStr = response.read().decode("utf-8")

        # check the response
        if json.loads(responseStr)["ok"]:
            print("Telegram sent to Chat ID: "+ CHAT_ID + ", Message (first 40 chars):" + message[0:40] + ", Formatting:" + parse + ", Silent:" + silentStr + ", DateTimeStamp:" + datetimestamp )
            print("Status OK: Details: " + responseStr)
        else:
            print('Error when sending Telegram message: Details: ' + responseStr)
            print('Sent details (ex API KEY): ' + HOST + URL + '/sendMessage' + json.dumps(payload))

# create an instance of sendsms
sendobj = sendtelegram()
# now send the message
sendobj.send(sys.argv)
quit()
