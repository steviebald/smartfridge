# Danyfan Carriage Smart Fridge

Control of relay based on temperature inside fridge, data logging and automatic sync of data to Github when Pi has an internet connection which will be infrequent via mobile hotspot

1) Python code to switch relay on and off when temp reaches threshold and log data to csv files rotated daily

2) Script to commit and push changes automatically to Github to sync logged data
Uses on ssh key to prevent username and password prompt each time
https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#platform-linux
https://stackoverflow.com/questions/21956750/secure-push-and-pull-with-no-password-git

3) Crontab entry to run gitsync.sh script every minute
* * * * * /home/pi/Desktop/python3/smartfridge/scripts/gitsync.sh &

4) /etc/rc.local entry to run smartfridge.py on startup
/usr/bin/python3 /home/pi/Desktop/python3/smartfridge/smartfridge.py &

