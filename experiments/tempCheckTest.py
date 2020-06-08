#!/usr/bin/env python3

'''tempCheckTest.py
Bix 8/21/18
Check RasPi Temp for Heatsink and Case tests
'''

# TEMP IS IN CELSIUS

import os, time, math, datetime

timeCounter = 1
temps, tempsTime, tempAvg, timeAvg = [], [], [], []
sessionStart = 0
tempHigh = 0
factNum = 55000
myNum = 1
outputFile = "tempCheckTest{myNum}.txt".format(myNum=myNum)

def measure_temp():
	temp = os.popen("vcgencmd measure_temp").readline()
	temp = temp.replace("temp=","")
	temp = temp.replace("'C\n", "")
	return temp

def logData(timeIn):
	f = open(outputFile, 'a')

	myTemp = sum(temps)/len(temps)
	tempAvg.append(myTemp)
	seshTempAvg = sum(tempAvg)/len(tempAvg)

	myTime = sum(tempsTime)/len(tempsTime)
	timeAvg.append(myTime)
	seshTimeAvg = sum(timeAvg)/len(timeAvg)

	f.write('Loop: ' + str(timeIn) + '\n')
	f.write('Session Length: ' + "{:.2f}".format((datetime.datetime.utcnow()-sessionStart).total_seconds()) + '\n')
	f.write('60Lo Avg Time: ' + "{:.2f}".format(myTime) + '\n')
	f.write('Session Avg Time: ' + "{:.2f}".format(seshTimeAvg) + '\n')
	f.write('60Lo Avg Temp: ' + "{:.2f}".format(myTemp) + '\n')
	f.write('Session Avg Temp: ' + "{:.2f}".format(seshTempAvg) + '\n')
	f.write('Session High: ' + "{:.2f}".format(tempHigh) + '\n\n')
	f.close()

f = open(outputFile, 'w')
sessionStart = datetime.datetime.utcnow()
f.write('Session Start (UTC): ' + str(sessionStart) + '\n\n')
f.close()

while True:
	myTemp = float(measure_temp())
	if myTemp > tempHigh:
		tempHigh = myTemp
		print('NEW HIGH')
	temps.append(myTemp)
	print(myTemp)
	startTime = datetime.datetime.utcnow()
	myFact = math.factorial(factNum) 
	endTime = datetime.datetime.utcnow()
	totTime = (endTime-startTime).total_seconds()
	tempsTime.append(totTime)
	print(totTime)

	if timeCounter % 60 == 0:
		logData(int(timeCounter/60))
		temps, tempsTime = [], []
		print('Inside')

	if timeCounter % 300 == 0:
		factNum = factNum * 2
		f = open(outputFile, 'a')
		f.write('Factorial Doubled To: ' + str(factNum) + '\n\n')
		f.close()

	timeCounter += 1
	print(timeCounter)
