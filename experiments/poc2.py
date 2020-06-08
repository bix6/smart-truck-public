# !/usr/bin/env python3

# poc2.py
# Bix 8/7/18
# Proof of Concept 2
# Extract Ticket #, Gallons and Timestamps
# Send Extracted Information to Cloud

import time, datetime, serial, struct

ser = serial.Serial(
	#port='COM3',
	#port='/dev/ttyUSB0',
	port='/dev/cu.usbserial',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=5
	)

logFile = open('poc2.txt', 'a') 
#cmdLastTrans = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'
#cmdLastTrans = b'\x7e\x01\xff\x48\x01\x2e\x00\x89\x7e'
cmdLastTrans = b'\x7e\x01\xff\x48\x01\x1a\x00\x9d\x7e'
cmdLastTransName = 'cmdLastTrans'
counter = 0
counterMax = 1
startStr = '---START---'
endStr = '---END---'
curTime = str(datetime.datetime.now().time())

print(startStr)
logFile.write(startStr + '\n')
print(curTime)
logFile.write(curTime + '\n')

while counter < counterMax:
	cmdOut = cmdLastTrans
	cmdName = cmdLastTransName

	ser.write(cmdOut)
	textOut = cmdName + ' Hex Out: ' + cmdOut.hex()
	print(textOut)
	logFile.write(textOut + '\n')

	bytesIn = ser.readline()
	textIn = cmdName + ' Hex In: ' + bytesIn.hex()
	print(textIn)
	logFile.write(textIn + '\n')

	saleNum = struct.unpack('<l', bytesIn[5:9])
	print('Sale Number: ' + str(saleNum[0]))
	logFile.write('Sale Number: ' + str(saleNum[0]) +'\n')

	startTime = []
	endTime = []
	for i in range (0, 6):
		startTime.append(struct.unpack('<B', bytesIn[31+i:32+i])[0])
		endTime.append(struct.unpack('<B', bytesIn[37+i:38+i])[0])

	startDateStr = 'Start Date: ' + str(startTime[4]) + '/' + str(startTime[2]) + '/' + str(startTime[5])
	print(startDateStr)
	logFile.write(startDateStr + '\n')

	startTimeStr = 'Start Time: ' + str(startTime[1]) + ':' + str(startTime[0]) + ':' + str(startTime[3])
	print(startTimeStr)
	logFile.write(startTimeStr + '\n')

	endDateStr = 'End Date: ' + str(endTime[4]) + '/' + str(endTime[2]) + '/' + str(endTime[5])
	print(endDateStr)
	logFile.write(endDateStr + '\n')

	endTimeStr = 'End Time: ' + str(endTime[1]) + ':' + str(endTime[0]) + ':' + str(endTime[3])
	print(endTimeStr)
	logFile.write(endTimeStr + '\n')

	totalizerBytes = [bytesIn[51:59], bytesIn[59:67], bytesIn[67:75], bytesIn[75:83]]
	totalizerNames = ['Totalizer Start', 'Totalizer End', 'Gross Volume', 'Volume']
	totalizerVals = []

	for b in totalizerBytes:
		totalizerVals.append(struct.unpack('<d', b)[0])

	for i in range (0,4):
		print(totalizerNames[i] + ': ' + str(totalizerVals[i]))
		logFile.write(totalizerNames[i] + ': ' + str(totalizerVals[i]) + '\n')

	counter += 1
	time.sleep(1)

curTime = str(datetime.datetime.now().time())
print(curTime)
logFile.write(curTime + '\n')
print(endStr)
logFile.write(endStr + '\n')