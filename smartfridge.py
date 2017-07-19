#To do
#Figure out how to synch log files
#cron to check if running and if not restart

from gpiozero import LED
import time 
from time import sleep
import os
import csv
import yaml

#load temperature drivers
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_fridge_sensor = "/sys/bus/w1/devices/28-80000002d084/w1_slave"
temp_external_sensor = "/sys/bus/w1/devices/28-80000002d31a/w1_slave"

LOGGING_FREQUENCY_SECS = 300
ERROR_TEMP = -273.0 #temperature to return if there is an error

relay = LED(14) #set up for a Normally Closed (NC) relay so switching it on actually switches the power off
led = LED(26) #status led
error = False

def getRaw(sensor):
	try:
		f = open(sensor, "r")
		lines = f.readlines()
		f.close()
	except:
		lines = "could find sensor";
		global error
		error = True
	return lines

def getTemperature(sensor):
	global ERROR_TEMP
	lines = getRaw(sensor)
	temp_c = ERROR_TEMP
	
	if lines[0].strip()[-3:] != "YES":
		print("error reading temperature sensor " + sensor)
	
	temp_output = lines[1].find("t=")
	
	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string)/1000.0
	
	return temp_c
		
def logData(fridgeThreshold, fridgeTemp, externalTemp, onOff):
	strTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	strDate = time.strftime('%Y%m%d', time.localtime())
	row = [strTime, fridgeThreshold, fridgeTemp, externalTemp, onOff]
	with open("/home/pi/Desktop/python3/smartfridge/data/"+strDate+".csv", "a") as f:
		w = csv.writer(f)
		w.writerow(row)

def getFridgeTempThreshold():
	config = yaml.load(file('/home/pi/Desktop/python3/smartfridge/config.yml', 'r'))
	print(config)
	return float(config["defaulttemp"])
	
#main code

while True:
	fridgeThreshold = getFridgeTempThreshold()
	tempFridge = getTemperature(temp_fridge_sensor)
	tempExternal = getTemperature(temp_external_sensor)

	led.on()
	print("Threshold: " + str(fridgeThreshold))
	print("Fridge temp: " + str(tempFridge))
	print("External temp: " + str(tempExternal))
	
	if tempFridge == ERROR_TEMP:
		led.blink(0.1,0.5)
		relay.off() #off for a NC relay = on
		print("error with fridge temp sensor fridge on")
		logData(fridgeThreshold, str(tempFridge), str(tempExternal), "error with fridge temp sensor fridge on")	
	elif tempFridge > fridgeThreshold:
		relay.off() #off for a NC relay = on
		print("fridge on")
		logData(fridgeThreshold, str(tempFridge), str(tempExternal), "on")
	else:
		relay.on() #on for a NC relay = off
		print("fridge off")
		logData(fridgeThreshold, str(tempFridge), str(tempExternal), "off")
			
	sleep(LOGGING_FREQUENCY_SECS)

