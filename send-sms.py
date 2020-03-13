#!/usr/bin/python3
#
# Function to send a SMS using the https://thesmsworks.co.uk/ provider. To be called from Domoticz rule. 
#
# Blochly Usage:    Start Script: <optional path to script>/send-sms.sh  
#                   with parameter(s): "<message text>" "<to number(s)>"  "<sender number or ID>" 
#                                      "<message tag>"  "<Y/N timestamp option"> 
#                                       - all arguements are optional and then defaults will apply
#                                       - provide null "" if subsequent arguements
#                   
# Argurements
# 1. message text   - sent as a single message of up to 160 characters or as multiple messages of 153 characters each.
#                     Read the providers notes about sending non GSM characters. Avoid copy and paste from Word etc.
#                     You  can send "+text" to append text to default message
#       Examples:   "My message"    =>  "My message"
#                   "" or omitted   =>  "DefaultMessage"
#                   "+extra text"   =>  "DefaultMessage extra text"
# 2. receipent(s) telephone no.s separated by commas. Do not start numbers international numbers with the + sign.
#       Examples:  "077123456"    =>  "077123456"
#                  "077123456,4477987654"    =>  "077123456,4477987654"
#                  "" or omitted   =>  "DefaultNumber"
# 3. sender - sender's telephone number OR identification that is between 3 and 11 characters with no spaces or special characters
#       Examples:   "0777891234"  =>  "0777891234",     "HMS"  =>  "HMS"
#                   "" or omitted =>  "DefaultSenderID"
# 4. message tag    - The tag can be alphanumeric and contain spaces. The maximum number of characters is 280 including spaces.
#       Examples:   "Heating Error"   =>  "Heating Error"
#                   "" or omitted =>  "DefaultTag"
# 5. datetimestamp - set to Y if the message is to be appended with a date and time stamp
#                   Format is according to the DATETIMEFORMAT setting
#       Examples when Y: and DATETIMEFORMAT= " at %Y-%m-%d %H:%M:%S"
#                   "My message text"   =>  "My message text at 2020-03-10 13:12:45"
#
# Future possible enhancements to include error handling and logging
#
# Version 2.1   
#       Removed MESSAGE_SCHED - messages to multiple receipients are sent using a loop
#       Added date & time stamp option
#       Convert message to GSM 03.38 encoding
#       Configutation setting are now in a send-sms-config.yml file
# AEC 2020-03-10
# License: GNU General Public License v3.0
#
# User setting are defined in the send-sms-config.yml file

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
with open(os.path.join(sys.path[0], "send-sms.yml"), 'r') as configfile:
    config = yaml.safe_load(configfile)

HOST = config["HOST"]
URL = config["URL"]
API_KEY = config["API_KEY"]
MESSAGE = config["MESSAGE"]
TO_TELNO = config["TO_TELNO"]
SENDER_ID = config["SENDER_ID"]
MESSAGE_TAG = config["MESSAGE_TAG"]
DATETIMESTAMP = config["DATETIMESTAMP"]
DATETIMEFORMAT = config["DATETIMEFORMAT"]

class sendsms:
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

        # to receipent(s) telephone numbers are an optional 2nd parameter
        # can be one or more numbers separated by commas
        if len(arguements) >= 3:
            toRecipientList = arguements[2]
            if toRecipientList != "":       # not null
                toRecipientList = arguements[2]
            else:
                toRecipientList = TO_TELNO
        else:
            toRecipientList = TO_TELNO
        
        # process each one
        toRecipients = toRecipientList.split(",")
        recipients = []
        for number in toRecipients:
            recipients.append(number)
        #print(recipients)

        # sender ID is an optional 3rd user arguement
        if len(arguements) >= 4:
            senderID = arguements[3]
            if senderID != "":       # not null
                senderID = arguements[3]
            else:
                senderID = SENDER_ID
        else:
            senderID = SENDER_ID

         # message tag is an optional 4th user arguement
        if len(arguements) >= 5:
            messageTag = arguements[4]
            if messageTag != "":       # not null
                messageTag = arguements[4]
            else:
                messageTag = MESSAGE_TAG
        else:
            messageTag = MESSAGE_TAG

        # datetimestamp is an optional 5th user arguement 
        if len(arguements) >= 6:
            if arguements[5] == "Y":   
                datetimestamp = "Y" 
            else:
                datetimestamp = "N" 
        else:
            datetimestamp = DATETIMESTAMP
        # apply datetimestamp option, either default or message override option
        if datetimestamp == "Y":
            now = datetime.now()
            message = message + now.strftime(DATETIMEFORMAT)

        # create the https request
        conn = http.client.HTTPSConnection(HOST)
        headers = {'Content-type': 'application/json', 'Authorization': API_KEY }
        
        # send to each recipient
        for recipient in recipients:
            # build the SMS message
            payload = {'sender': senderID, 'destination': recipient, 'content': message, 'tag': messageTag, 'ttl': 10 }
            json_data = json.dumps(payload)
        
            # build the POST message
            conn.request('POST', URL, json_data, headers)
        
            # send the SMS message
            response = conn.getresponse()
            if response.status >= 200 and response.status < 300:
                print("SMS sent: To: "+ recipient + ", From: " + senderID + ", Message (first 40 chars):" + message[0:40] + ", Tag:" + messageTag)  
                print("Status OK:" + str(response.status) + ", details: "+ response.read().decode("utf-8"))
            elif response.status >= 300 and response.status < 400:
                print('Redirection Error when sending SMS message ' + str(response.status) + ',details:' + response.read().decode("utf-8"))
                print("See https://thesmsworks.co.uk/developers#errors")
            elif response.status >= 400 and response.status < 500:
                print('Client Error when sending SMS message ' + str(response.status) + ',details:' + response.read().decode("utf-8"))
                print("See https://thesmsworks.co.uk/developers#errors")
            else:
                print('Server Error when sending SMS message ' + str(response.status) + ',details:' + response.read().decode("utf-8"))
                print("See https://thesmsworks.co.uk/developers#errors")

# create an instance of sendsms
sendobj = sendsms()
# now send the message
sendobj.send(sys.argv)
quit()
