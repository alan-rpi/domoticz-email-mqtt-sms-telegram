#!/usr/bin/python3
#
# Function to send an email. To be called from Domoticz rule
#
# Blochly Usage:    Start Script: <optional path to script>/hms-send-email.sh  
#                   with parameter(s): "<message>" "<subject>" "<email address>"     
#                                       - all arguements are optional and then defaults will apply
#                                       - provide null "" if subsequent arguements
#                   
#
# 1st arguement: message text
#       Examples:   "My message"    =>  "My message"
#                   "" or omitted   =>  "DefaultMessage"
# 2nd optional arguement: subject - can send "+text" to append text to default subject. Set to "" if having a 3rd and no 2nd arguenment.
#       Examples:   "Alarm Alert"  =>  "Alarm Alert",  "+Warning"  =>  "Default Subject Warning", 
#                   "" or omitted  =>  "Default Subject"
# 3rd optional arguement: email addresses(s) either full addresses separated by commas or recipient name(s) with the @domain as per TO_ADDRESS.
#       Examples:   "" or omitted =>  "defaultname<defaultname@defaultdomain.com>"
#                   "realname<thisname@thisdomain.com>" =>  "realname<thisname@thisdomain.com>"
#                   "thisname"  =>  "<thisname@defaultdomain.com>"
#                   "thisname1,thisname2"   =>  "<thisname1@defaultdomain.com>,<thisname2@defaultdomain.com>"
#
# Future possible enhancements to include error handling, logging, SSL 
#
# Version 2
# AEC 2020-03-05
# License: GNU General Public License v3.0
#
HOST = 'auth.smtp.my-ISP-domain.co.uk'         
PORT = 587                                   
LOGIN_ADDRESS = 'myname@my-email-domain.me.uk' 
PASSWORD = 'my-password'
FROM_ADDRESS = 'My Name<my-name@myemail-domain.me.uk>'
TO_ADDRESS = 'Recipient Name<recipient-name@their-email-addr.me.uk>' # exclude the real name and <> if parameter 3 is provided
SUBJECT = "My Subject"      # default subject. 
MESSAGE = "My Message"      # default message. 

# No user setting beyond this line

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

class sendemail:
    def __init__(self):
        pass

    def send(self, arguements):
        # message is an optional 1st user arguement
        if len(arguements) >= 2:
            message = arguements[1]
            if message != "":       # not null
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
