#!/bin/bash  

timestamp=$(date +%T)

cd /home/pi/Desktop/python3/smartfridge/
git --git-dir /home/pi/Desktop/python3/smartfridge/.git add .
git --git-dir /home/pi/Desktop/python3/smartfridge/.git commit -m $timestamp
git --git-dir /home/pi/Desktop/python3/smartfridge/.git push
echo "done"
