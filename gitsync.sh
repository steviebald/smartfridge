#!/bin/bash  

current_date_time = date + "%Y-%m-%d %H:%M:%S";

cd /home/pi/Desktop/python3/smartfridge/
git --git-dir /home/pi/Desktop/python3/smartfridge/.git add .
git --git-dir /home/pi/Desktop/python3/smartfridge/.git commit -m $current_date_time
git --git-dir /home/pi/Desktop/python3/smartfridge/.git push
echo "done"
