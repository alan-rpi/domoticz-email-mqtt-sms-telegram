# domoticz-email-mqtt
Simple scripts to send email and mqtt messages from Domoticz Blockly rules

## Overview
These scripts were created to overcome 2 issues when running a Docker Domoticz container:

1. When using the [joshuacox/mkdomoticz](https://github.com/joshuacox/mkdomoticz) image Domoticz failed to send emails. A number of people have raise an issue. Meanwhile the email script in this repository is a workaround.

2. When using Domoticz Blockly, the visual Rule engine, there was no MQTT component to publish a mqtt message. The mqtt script in this repository is a workaround.

These scripts may be used together or separately. Each of the 2 solutions consists of a Python script and a Bash script. They can also be used on a non Docker system.

## Requirements
domoticz
python paho-mqtt

Note: the scripts were developed for use on a Domoticz Docker container. They were tested on a Raspberry Pi 4 with Buster.

### Main Limitations
Neither the email or the mqtt publish scripts support SSL. Also there is no logging or error checking. See Limitations below for more information.

## Contributing
Feel free to make an issue or pull request [here](https://github.com/alan-rpi/domoticz-email-mqtt). As this is a hobby project response times are not guaranteed.

# Implementation
Download the scripts to a Linux machine and edit using your favourite editor (e.g. nano or vi) edit the user settings as described below. Do not edit on a Windows PC as the new line (CR) format upsets Linux. On a Windows PC you can use Visual Studio and access the files via a shared folder.

## Email Bash Scripts send-email-template.sh and send-mqtt-template.sh 
After downloading edit the script to set the path to the python script relative to the invokded folder in Domoticz. This has been tested on a system where they were stored within the user's mapped folder defined in the Docker run command or the Docker compose file, e.g.
```
volumes:
      - /home/pi/docker/domoticz-data:/config
```
and then the Bash script file contains:
```
      python3 /config/hms-send-email.py "$@"
or    python3 /config/hms-send-mqtt.py "$@"
```
With this method the Rules within Domoticz will need prefixing with "/config/". The advantage is that the script can be edited from a Windows PC with Visual Studio using a share to the mapped folder on the machine running Docker.

Alternatively, store the scripts within the default location for Domoticz scripts which the author believes is "/src/domoticz/scripts/" within the Domoticz container. No path should be needed if the python scripts are in the same folder. Note the author has only tried the mapped folder method.

Rename the Bash script to send-email.sh / send-mqtt.sh as appropriate, and change the permissions with:
```
    chmod 771 send-email.sh 
or  chmod 771 send-mgtt.sh 
```
This is because the scripts will be run under root within Domoticz but they will belong to your user ID.

## Email Python Scripts send-email-template.py and send-mqtt-template.py
As above with the bash sh scripts, download, edit, rename without "-template" and set permissions and store either in the user's mapped folder or in the Domoticz default /domoticz/scripts/lua folder or if using Domoticz's editor then they are stored in the database. Note the author has only tried the mapped folder method.
 
## send-email-template.py
Set the values of the 8 user defined variables. These include default values. Note that the email account password is defined within the script so take steps to ensure that the file permission retrict access to this file. See Limitations below.

### Limitations
There is no SSL support, logging or error checking. The script could be enhanced to provide these so long as there was backward compatiability.

### Dependencies
None known

## send-mqtt-template.py
Set the values for the 8 user defined variables. These include the default values. See Limitations below.

### Limitations
The QOS, RETAIN, SSL_CERT and SSL_TLS are are fixed within the script. Also there is no logging or error checking. The script could be enhanced to provide these so long as there was backward compatiability. 

### Dependencies
You will need to install a python mqtt client within the Domoticz container. Portainer provides a CLI window into the container where you can run the install commands:
```
apt-get update 
apt-get install python3-pip
pip3 install paho-mqtt
```
# Usage

## send-email

Blochly Usage:      Start Script: <optional path to bash script>/send-email.sh  
                    with parameter(s): "<message>" "<subject>" "<email address>"     
                                       - all arguements are optional and then defaults will apply
                                       - provide null "" if subsequent arguements

If your Bash scripts are within the container's mapped path to a user's folder then set the Bash's path and script name to:
```
/config/send-email.sh 
```
otherwise, where the script is in Domoticz's database or the /domoticz/scripts/lua folder, then simiply give the script name:
 ```
send-email.sh 
```

 1st arguement: message text
       Examples:   "My message"    =>  "My message"
                   "" or omitted   =>  "DefaultMessage"
 2nd optional arguement: subject - you can prefix with "+" to append to default subject. Set to "" if having a 3rd and no 2nd arguenment.
       Examples:   "Alarm Alert"  =>  "Alarm Alert",  "+Warning"  =>  "Default Subject Warning", 
                   "" or omitted  =>  "Default Subject"
 3rd optional arguement: email addresses(s) either full addresses separated by commas or recipient name(s) with the @domain as per the default TO_ADDRESS.
       Examples:   "" or omitted =>  "defaultname<defaultname@defaultdomain.com>"
                   "realname<thisname@thisdomain.com>" =>  "realname<thisname@thisdomain.com>"
                   "thisname"  =>  "<thisname@defaultdomain.com>"
                   "thisname1,thisname2"   =>  "<thisname1@defaultdomain.com>,<thisname2@defaultdomain.com>"

## send-mqtt
 Blochly Usage:    Start Script: <optional path to bash script>/send-mqtt.sh  
                   with parameter(s): "<topic>" "<value>"
                                       - all arguements are optional and then defaults will apply
                                       - provide null "" if subsequent arguements

If your Bash scripts are within the container's mapped path then set the Bash's path and script name to:
```
/config/send-mqtt.sh
```
otherwise where the script is in Domoticz's database or the /domoticz/scripts/lua folder then simiply give the script name:
 ```
send-mqtt.sh 
```

 1st arguement: topic  - you can prefix with "+" to append the topic to the default topic
   Examples:   "MyTopic/SubTopicA"     => "MyTopic/SubTopicA"
               "+SubTopicB"            => "DefaultTopic/DefaultSubTopic/SubTopicB"
               "" or omitted           => "DefaultTopic/DefaultSubTopic"
 2nd arguement: value 
   Examples:   "0"     => "0"
               ""      => "DefaultValue"

## Testing
Both the Bash and Python scripts can be tested via the command line and this will display any errors. Make sure the paths are correct for both the CLI command and within the Bash sh. script. E.g.
 ```
      python3 /config/hms-send-mqtt.py "hms/alert" "test mqtt value"
or    /config/hms-send-email.sh "test email message" "test subject" "test@emailaddress.com"
```
