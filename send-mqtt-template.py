#!/usr/bin/python3
#
# Function to send a MQTT message. To be called from Domoticz rule
#
# Blochly Usage:    Start Script: <optional path to script>/hms-send-mqtt.sh  
#                   with parameter(s): "<topic>" "<value>"
#                                       - all arguements are optional and then defaults will apply
#                                       - provide null "" if subsequent arguements
#
# 1st arguement: topic  - can prefix with "+" to append the topic to the default topic
#   Examples:   "MyTopic/SubTopicA"     => "MyTopic/SubTopicA"
#               "+SubTopicB"            => "MyTopic/SubTopicA/SubTopicB"
#               "" or omitted           => "DefaultTopic/DefaultSubTopic"
# 2nd arguement: value 
#   Examples:   "0"     => "0"
#               ""      => "DefaultValue"
#
# Future possible enhancements to include error handling, logging, QOS, retain arguement and SSL
#   e.g.  publish(topic, payload=None, qos=0, retain=False)
# For more debugging code see https://www.programcreek.com/python/example/106505/paho.mqtt.client.Client
#
# Version 2
# AEC 2020-03-05
# License: GNU General Public License v3.0

HOST = '192.168.x.xx'   # IP address of your MQTT Broker
PORT = 1883             # and its port, usually 1883
TOPIC = "mytopic/alert" # default Topic
VALUE = "0"             # default Value
QOS = 0                 # default Quality of Service is fixed for now. 0 means the Broker does not send a delivery receipt
RETAIN = False          # default Retain is fixed false for now
SSL_CERT = ""           # default Path & filename of the certificate. Currently not supported
SSL_TLS = 2             # default TLS version. Currently not supported
# No user setting beyond this line

import paho.mqtt.client as paho
import sys

def on_publish(client,userdata,result):     # create function for callback
    print("Data published - no acknowledgement as QOS=0. Result=" + str(result) + " \n")  # userdata is object
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

        # create client object
        client1 = paho.Client("hms")
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


