#!/usr/bin/python3
#
# Function to send a MQTT message. To be called from Domoticz rule
#
# Blochly Usage:    Start Script: <optional path to script>/send-mqtt.sh  
#                   with parameter(s): "<topic>" "<value>" "Y/N datetime stamp"
#                         - all arguements are optional and then defaults will apply
#                         - provide null "" if subsequent arguements
#
# Arguements:
# 1. topic  - can prefix with "+" to append the topic to the default topic
#   Examples:   "MyTopic/SubTopicA"     => "MyTopic/SubTopicA"
#               "+SubTopicB"            => "MyTopic/SubTopicA/SubTopicB"
#               "" or omitted           => "DefaultTopic/DefaultSubTopic"
# 2. value 
#   Examples:   "0"     => "0"
#               ""      => "DefaultValue"
# 3. datetimestamp - set to Y if the Value is to be appended with a date and time stamp
#                   Format is according to the DATETIMEFORMAT setting
#       Examples when Y: and DATETIMEFORMAT = " at %Y-%m-%d %H:%M:%S"
#                   "My value text"   =>  "My value text at 2020-03-10 13:12:45"
#
#
# Future possible enhancements to include error handling, logging, QOS, retain arguement and SSL
#   e.g.  publish(topic, payload=None, qos=0, retain=False)
# For more debugging code see https://www.programcreek.com/python/example/106505/paho.mqtt.client.Client
#
# Version 2.1
#       Added date & time stamp option
#       Configutation setting are now in a send-mqtt-config.yml file
# AEC 2020-03-05
# License: GNU General Public License v3.0

import paho.mqtt.client as paho     # pip3 install paho-mqtt
import sys
import os
from datetime import datetime
import yaml                         # apt-get install python-yaml

# get configuration settings
with open(os.path.join(sys.path[0], "send-mqtt.yml"), 'r') as configfile:
    config = yaml.safe_load(configfile)

HOST = config['HOST']
PORT = config['PORT']
CLIENT_ID = config['CLIENT_ID']
TOPIC = config['TOPIC']
VALUE = config['VALUE']
QOS = config['QOS']
RETAIN = config['RETAIN']
SSL_CERT = config['SSL_CERT']
SSL_TLS = config['SSL_TLS']
DATETIMESTAMP = config['DATETIMESTAMP']
DATETIMEFORMAT = config['DATETIMEFORMAT']

def on_publish(client,userdata,result):     # create function for callback
    pass

class sendmqtt:
    def __init__(self):
        pass

    def send(self, arguements):

        # message text is passed as the 1st arguement
        if len(arguements) >= 2:
            topic = arguements[1]
            if topic != "":       # not null
                if topic[0:1] == "+":
                    topic = TOPIC + '\\' + topic[1:]
                else:
                    topic = arguements[1]
            else:
                topic = TOPIC
        else:
            topic = TOPIC
        
        # value  is passed as the 2nd arguement
        if len(arguements) >= 3:
            value = arguements[2]
        else:
            value = VALUE                 

        # datetimestamp is an optional 3rd user arguement 
        if len(arguements) >= 4:
            if arguements[3] == "Y":   
                datetimestamp = "Y" 
            else:
                datetimestamp = "N" 
        else:
            datetimestamp = DATETIMESTAMP
        # apply datetimestamp option, either default or override option
        if datetimestamp == "Y":
            now = datetime.now()
            value = value + now.strftime(DATETIMEFORMAT)
        
        # create client object
        client1 = paho.Client(CLIENT_ID)
        # assign function to callback
        client1.on_publish = on_publish
        # establish connection
        client1.connect(HOST,PORT)
        # publish
        retcode = client1.publish(topic,value)
        print("Sent Topic: "+ topic + ", Value: " + value + ". Return was:" + str(retcode))

# create an instance of sendmqtt
sendobj = sendmqtt()
# now send the message
sendobj.send(sys.argv)
quit()
