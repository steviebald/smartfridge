# Danyfan Carriage smart fridge, data logging and automatic sync of data to Github when Pi has an internet connection
1) Python code to switch relay on and off when temp reaches threshold and log to csv file
2) Script to commit and push changes automatically to Github to sync logged data
3) Crontab entry to run gitsync.sh script every minute
4) /etc/rc.local entry to run smartfridge.py on startup
