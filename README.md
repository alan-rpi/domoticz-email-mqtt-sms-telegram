# domoticz-email-mqtt-sms-telegram
Simple scripts to send email, mqtt, sms and telegram messages from Domoticz Blockly rules

## Overview
These scripts were created to overcome 4 issues when running a Docker Domoticz container:

1. When using the [joshuacox/mkdomoticz](https://github.com/joshuacox/mkdomoticz) image Domoticz failed to send emails. A number of people have raise an issue. Meanwhile the email script in this repository is a workaround and provides various command line options.

2. When using the [joshuacox/mkdomoticz](https://github.com/joshuacox/mkdomoticz) image Domoticz failed to send Telegram messages. The email script in this repository is a workaround and provides various command line options.

3. When using Domoticz Blockly, the visual Rule engine, there was no MQTT component to publish a mqtt message. The mqtt script in this repository is a workaround.

4. Whilst there was an Domoticz Blockly SMS component it was tied to a US company. This SMS script is linked to a UK company, thesmsworks.co.uk . This company has been used by the author for testing but users should make their own evaluation as to the suitability, compentancies and pricing model of the company. The configuration file does allow another SMS service provider to be specified but whether the script will work is unknown.

These scripts may be used together or separately. Each of the 3 solutions consists of a Python script, a Yaml Configuration file, and a Bash script. They can also be used on a non Docker system.

## Requirements
domoticz
python paho-mqtt        for mqtt
python-yaml             for sms, mqtt, email and telegram

http.client, datetime, time, sys, os, pprint, smtplib, MIMEMultipart and MIMEText should all be part of a standard python package.

The above will need to be installed. If using Docker then installed within the container.

Note: the scripts were developed for use on a Domoticz Docker container. They were tested on a Raspberry Pi 4 with Buster.

### Main Limitations
Neither the email or the mqtt publish scripts support SSL. Also there is no logging or error checking. See Limitations below for more information.

## Contributing
Feel free to make an issue or pull request [here](https://github.com/alan-rpi/domoticz-email-mqtt). As this is a hobby project response times are not guaranteed.

# Implementation
Download the scripts to a Linux machine and edit using your favourite editor (e.g. nano or vi) edit the user settings as described below. Do not edit on a Windows PC as the new line (CR) format upsets Linux. On a Windows PC you can use Visual Studio and access the files via a shared folder.

## Bash Scripts send-email.sh, send-mqtt.sh, send-sms.sh and send-telegram.sh 
After downloading edit the script to set the path to the python script relative to the invoked folder in Domoticz. This has been tested on a system where they were stored within the user's mapped Volumes folder defined in the Docker run command or the Docker compose file, e.g.
```
volumes:
      - /home/pi/docker/domoticz-data:/config
```
and then the Bash script files contain:
```
      python3 /config/send-email.py "$@"
      python3 /config/send-mqtt.py "$@"
      python3 /config/send-sms.py "$@"
      python3 /config/send-telegram.py "$@"
```
With this method the Blockly Rules within Domoticz will need prefixing with "/config/". The advantage is that the script can be edited from a Windows PC with Visual Studio using a share to the mapped folder on the machine running Docker. If you chose this option then the Bash .sh files do not need to be editted.

Alternatively, store the scripts within the default location for Domoticz scripts which the author believes is "/src/domoticz/scripts/" within the Domoticz container. No path should be needed if the python scripts are in the same folder. Note the author has only tried the mapped folder method.

Ensure the .sh files have the correct execute permissions with:
```
    sudo chmod 771 send-email.sh 
    sudo chmod 771 send-mgtt.sh 
    sudo chmod 771 send-sms.sh 
    sudo chmod 771 send-telegram.sh 
```
This is because the scripts will be run under root within Domoticz but they will belong to your user ID.

## Python Scripts send-email.py, send-mqtt.py, send-sms.py and send-telegram.py
As above with the bash .sh scripts, download, set the same permissions and store either in the user's mapped folder, or in the Domoticz default folder, or if using Domoticz's editor then they are stored in the database. Note the author has only tried the mapped folder method. These files do not need editting.

## Python Yaml Configuration files send-email-template.yml, send-mqtt-template.yml, send-sms-template.yml and send-telegram-template.yml
 Download these and store in the same folder at the python scripts. Edit the files and set your own configuation values and then save without the "-template" suffix.  They should have permission of 760 so that the only the user pi and group can edit them and others cannot read or edit them.
```
      sudo chmod 760 send-email.yml 
      sudo chmod 760 send-mgtt.yml
      sudo chmod 760 send-sms.yml
      sudo chmod 760 send-telegram.yml
```

### send-email.py Limitations
There is no SSL support, logging or error checking in this script. The script could be enhanced to provide these so long as there was backward compatiability.

### Dependencies
python-yaml needs to be installed within the Domoticz container. Portainer provides a CLI window into the container where you can run the install commands:
```
apt-get update 
apt-get install python-yaml
```
If the container is freshly downloaded then you will need to repeat the install.

## send-mqtt.py Limitations
The QOS, RETAIN, SSL_CERT and SSL_TLS are are fixed within the script. Also there is no logging or error checking. The script could be enhanced to provide these so long as there was backward compatiability. 

### Dependencies
You will need to install a python mqtt client and python-yaml within the Domoticz container. Portainer provides a CLI window into the container where you can run the install commands:
```
apt-get update 
apt-get install python3-pip
pip3 install paho-mqtt
apt-get install python-yaml
```
If the container is freshly downloaded then you will need to repeat the install.

## send-sms.py Limitations
Whilst configuration setting have been provided for Host & URL they have only been tested with thesmsworksco.uk service provider. Also there is no logging and limtted error checking. The script could be enhanced to provide these so long as there was backward compatiability. 

### Dependencies
You will need to install python-yaml within the Domoticz container. Portainer provides a CLI window into the container where you can run the install commands:
```
apt-get update 
apt-get install python-yaml
```
If the container is freshly downloaded then you will need to repeat the install.

## send-telegram.py Limitations
There is no support for disable_web_page_preview, reply_to_message_id and reply_markup parameters. There is no logging and limtted error checking. The script could be enhanced to provide these so long as there was backward compatiability.

### Dependencies
You will need to install python-yaml within the Domoticz container. Portainer provides a CLI window into the container where you can run the install commands:
```
apt-get update 
apt-get install python-yaml
```
If the container is freshly downloaded then you will need to repeat the install.

## Passwords
Note that the email account password, sms API key and telegram API key and chat ID are defined within the configuration files so take steps to ensure that the file permission retrict access to these files.

# Usage

## send-email

Blochly Usage:      Start Script: <optional path to bash script/>send-email.sh  
                    with parameter(s): "<message>" "<subject>" "<email address(s)>" "<Y/N timestamp option">    
                        - all arguements are optional and then defaults will apply
                        - provide null "" if there are subsequent arguements

Arguement values: See the comments at the start of the python script. Some arguements allow a "+" prefix to suffix the default value.

## send-mqtt
 Blochly Usage:    Start Script: <optional path to bash script/>send-mqtt.sh  
                   with parameter(s): "<topic>" "<value>" "<Y/N timestamp option">    
                        - all arguements are optional and then defaults will apply
                        - provide null "" if there are subsequent arguements

Arguement values: See the comments at the start of the python script. Some arguements allow a "+" prefix to suffix the default value.

## send-sms
 Blochly Usage:    Start Script: <optional path to bash script/>send-sms.sh  
                   with parameter(s): "<message text>" "<to number(s)>"  "<sender number or ID>"  
                                      "<message tag>"  "<Y/N timestamp option"> 
                        - all arguements are optional and then defaults will apply
                        - provide null "" if there are subsequent arguements

Arguement values: See the comments at the start of the python script. Some arguements allow a "+" prefix to suffix the default value.

## send-telegram
Blochly Usage:    Start Script: <optional path to script>/send-telegram.sh  
                   with parameter(s): "<message text>" "<chat ID>" "<parse option>"                   "<Y/N silent option>"  "<Y/N timestamp option"> 
                        - all arguements are optional and then defaults will apply
                        - provide null "" if subsequent arguements
                   
## Testing
Both the Bash and Python scripts can be tested via the command line and this will display any errors. Make sure the paths are correct for both the CLI command and within the Bash sh. script. E.g.
 ```
      cd /home/pi/docker/domoticz-data:/config
      python3 send-mqtt.py "hms/alert" "garage door is open"
or    send-email.sh "garage door is open" "hms alert" "me@emailaddress.com"
or    python3 send-sms.py "hms alert - garage door is open" "077123456,072345678"
or    send-telegram.sh "<b>hms alert</b> - garage door is open" "" "html"
```

