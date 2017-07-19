#!/bin/sh

ps auxw | grep smartfridge.py | grep -v grep > /dev/null

if [ $? != 0 ]
then
	/usr/bin/python /home/pi/Desktop/python3/smartfridge/smartfridge.py > /dev/null &
fi
