#!/usr/bin/python3
#
# Function to send an email. To be called from Domoticz rule
#
# Blochly Usage:    Start Script: <optional path to script>/send-email.sh  
#                   with parameter(s): "<message>" "<subject>" "<email address>"  "Y/N datetime stamp"
#                                       - all arguements are optional and then defaults will apply
#                                       - provide null "" if subsequent arguements
#
# 1. message text can send "+text" to append text to default message text. 
#       Examples:   "My message"    =>  "My message"
#                   "" or omitted   =>  "DefaultMessage"
#                   "+extra text"   =>  "DefaultMessage extra text"
# 2. subject - can send "+text" to append text to default subject. 
#       Examples:   "Alarm Alert"  =>  "Alarm Alert",  "+Warning"  =>  "Default Subject Warning", 
#                   "" or omitted  =>  "Default Subject"
# 3. email addresses(s) either full addresses separated by commas or recipient name(s) with the @domain as per TO_ADDRESS.
#       Examples:   "" or omitted =>  "defaultname<defaultname@defaultdomain.com>"
#                   "realname<thisname@thisdomain.com>" =>  "realname<thisname@thisdomain.com>"
#                   "thisname"  =>  "<thisname@defaultdomain.com>"
#                   "thisname1,thisname2"   =>  "<thisname1@defaultdomain.com>,<thisname2@defaultdomain.com>"
# 4. datetimestamp - set to Y if the message is to be appended with a date and time stamp
#                   Format is according to the DATETIMEFORMAT setting
#       Examples when Y: and DATETIMEFORMAT= " at %Y-%m-%d %H:%M:%S"
#                   "My message text"   =>  "My message text at 2020-03-10 13:12:45"
#
# Future possible enhancements to include error handling, logging, SSL 
#
# Version 2.1   
#       Added date & time stamp option
#       Configutation setting are now in a send-email-config.yml file
# Version 2.2
#       applied .upper() to datetimestamp 
# AEC 2020-03-14
# License: GNU General Public License v3.0
#
# User setting are defined in the send-sms-config.yml file

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import os
from datetime import datetime
import yaml         # sudo apt-get install python-yaml

# get configuration settings
with open(os.path.join(sys.path[0], "send-email.yml"), 'r') as configfile:
    config = yaml.safe_load(configfile)

HOST = config['HOST']
PORT = config['PORT']
LOGIN_ADDRESS = config['LOGIN_ADDRESS']
PASSWORD = config['PASSWORD']
TO_ADDRESS = config['TO_ADDRESS']
FROM_ADDRESS = config['FROM_ADDRESS']
SUBJECT = config['SUBJECT']
MESSAGE = config['MESSAGE']
DATETIMESTAMP = config['DATETIMESTAMP']
DATETIMEFORMAT = config['DATETIMEFORMAT']

class sendemail:
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
        
        # subject is an optional 2nd user arguement
        if len(arguements) >= 3:
            subject = arguements[2]
            if subject != "":       # not null
                # if 1st character is a + then append to the default SUBJECT
                if subject[0:1] == "+":
                    subject = SUBJECT + " " + subject[1:]
                else:
                    subject = arguements[2]
            else:
                subject = SUBJECT
        else:
            subject = SUBJECT

        # to addresses are an optional 3rd parameter
        # may be one or more email addresses, either full or just names, separated by commas
        
        if len(arguements) >= 4:
            if arguements[3] == "":    
                toAddressList = TO_ADDRESS
            else:    
                toAddressList = arguements[3]
        else:
            toAddressList = TO_ADDRESS
        toAddresses = toAddressList.split(",")

        # process each one
        comma = ""
        newAddressList = ""
        for address in toAddresses:
            # see if full adddresses or just name
            splitAddress = address.split("@")
            if len(splitAddress) == 2:   # full address name@domain
                thisAddress = address
            else:                       # name w/o domain
                splitToDomain = TO_ADDRESS.split("@")
                thisAddress = "<" + splitAddress[0]+"@"+splitToDomain[1]
            # build list
            newAddressList = newAddressList + comma + thisAddress
            comma = ", "
        #print(newAddressList , subject)

        # datetimestamp is an optional 4th user arguement 
        if len(arguements) >= 5:
            if arguements[4].upper() == "Y":   
                datetimestamp = "Y" 
            else:
                datetimestamp = "N" 
        else:
            datetimestamp = DATETIMESTAMP.upper()
        # apply datetimestamp option, either default or message override option
        if datetimestamp == "Y":
            now = datetime.now()
            message = message + now.strftime(DATETIMEFORMAT)

        # set up the SMTP server
        s = smtplib.SMTP(HOST, PORT)
        s.starttls()
        s.login(LOGIN_ADDRESS, PASSWORD)
        
        # create a message and add the attributes
        msg = MIMEMultipart()       
        msg['To']=newAddressList
        msg['From']=FROM_ADDRESS
        msg['Subject']=subject
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        # Terminate the SMTP session and close the connection
        s.quit()

        print("Email sent. To: "+ newAddressList + ", From: " + FROM_ADDRESS + ", Subject: " + subject + ", Message (first 40 chars):" + message[0:40])

# create an instance of sendemail
sendobj = sendemail()
# now send the message
sendobj.send(sys.argv)
quit()
