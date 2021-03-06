#To do
#Figure out how to synch log files
#cron to check if running and if not restart

from gpiozero import LED
import time 
from time import sleep
import os
import csv
import yaml
from datetime import datetime

#load temperature drivers
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_fridge_sensor = "/sys/bus/w1/devices/28-80000002d084/w1_slave"
temp_external_sensor = "/sys/bus/w1/devices/28-80000002d31a/w1_slave"

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
#check if current time is in any of the 2 zones else return default
def getFridgeTempThreshold():
	#config = yaml.load(file('/home/pi/Desktop/python3/smartfridge/config.yml', 'r'))
	temp = ""
	
	start1 = datetime.strptime(config["zone1"]["start"], "%H:%M:%S").time()
	end1 = datetime.strptime(config["zone1"]["end"], "%H:%M:%S").time()
	start2 = datetime.strptime(config["zone2"]["start"], "%H:%M:%S").time()
	end2 = datetime.strptime(config["zone2"]["end"], "%H:%M:%S").time()
	
	if (time_in_range(start1, end1, datetime.now().time())):
		temp = config["zone1"]["temp"]
		print("time is in zone 1")
	elif (time_in_range(start2, end2, datetime.now().time())):
		temp = config["zone2"]["temp"]
		print("time is in zone 2")
	else:
		temp = config["defaulttemp"]
		print("time is not in a zone, using default")
	
	return float(temp)
	
def time_in_range(start, end, x):
    	"""Return true if x is in the range [start, end]"""
	print(start)
	print(end)
	print(x)
    	if start <= end:
        	return start <= x <= end
    	else:
        	return start <= x or x <= end

#main code

while True:
        config = yaml.load(file('/home/pi/Desktop/python3/smartfridge/config.yml', 'r'))

	frequencySecs = int(config["frequencysecs"])
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
			
	sleep(frequencySecs)

