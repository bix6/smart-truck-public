#!/usr/bin/env python3

'''tempCheck.py
Bix 8/20/18
Check RasPi Temp
https://medium.com/exploring-code/monitor-the-core-temperature-of-your-raspberry-pi-3ddfdf82989f
'''

# TEMP IS IN CELSIUS

import os
import time

timeCounter = 1
tempsTen = []
tempsSixty = []

def measure_temp():
	temp = os.popen("vcgencmd measure_temp").readline()
	temp = temp.replace("temp=","")
	temp = temp.replace("'C\n", "")
	return temp

def logOne(timeIn, tempIn):
	f = open('tempCheck1.txt', 'a')
	f.write(str(timeIn) + ': ' + str(tempIn) + '\n')
	f.close()

def logTen(timeIn, tempIn):
	f = open('tempCheck10.txt', 'a')
	f.write(str(timeIn) + ': ' + str(tempIn) + '\n')
	f.close()

def logSixty(timeIn, tempIn):
	f = open('tempCheck60.txt', 'a')
	f.write(str(timeIn) + ': ' + str(tempIn) + '\n')
	f.close()

def logTenAvg(timeIn):
	f = open('tempCheck10Avg.txt', 'a')
	myAvg = sum(tempsTen)/len(tempsTen)
	f.write(str(timeIn) + ': ' + str(myAvg) + '\n')
	f.close()

def logSixtyAvg(timeIn):
	f = open('tempCheck60Avg.txt', 'a')
	myAvg = sum(tempsSixty)/len(tempsSixty)
	f.write(str(timeIn) + ': ' + str(myAvg) + '\n')
	f.close()

while True:
	myTemp = float(measure_temp())
	tempsTen.append(myTemp)
	tempsSixty.append(myTemp)
	print(myTemp)
	logOne(timeCounter, myTemp)
	if timeCounter % 10 == 0:
		logTen(timeCounter / 10, myTemp)
		logTenAvg(timeCounter / 10)
		tempsTen = []
	if timeCounter % 60 == 0:
		logSixty(timeCounter / 60, myTemp)
		logSixtyAvg(timeCounter / 60)
		tempsSixty = []
	time.sleep(1)
	timeCounter += 1