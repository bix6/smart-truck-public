# !/usr/bin/env python3

# poc.py
# Bix 8/6/18
# Proof of Concept
# Extract Ticket #, Gallons and Timestamps
# Send Extracted Information to Cloud

import time, datetime, serial, os, sys, struct, binascii

ser = serial.Serial(
	#port='COM3',
	#port='/dev/ttyUSB0',
	port='/dev/cu.usbserial',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=5 #TODO experiment with this. Emulator uses 5s?
	)

logFile = open('poc.txt', 'a') 
cmdLastTrans = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'
cmdLastTransName = 'cmdLastTrans'
counter = 0
counterMax = 2
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
	textOut = cmdName + ' Out: ' + cmdOut.hex()
	print(textOut)
	logFile.write(textOut + '\n')

	bytesIn = ser.readline()
	textIn = cmdName + ' In: ' + bytesIn.hex()
	print(textIn)
	logFile.write(textIn + '\n')

	hexBytes = bytesIn.hex()
	saleNumBytes = hexBytes[10:18]
	saleNum = struct.unpack('<l', binascii.unhexlify(saleNumBytes))
	print('Sale Number: ' + str(saleNum[0]))
	logFile.write('Sale Number: ' + str(saleNum[0]) +'\n')

	startTimeBytes = hexBytes[62:74]
	minute = struct.unpack('<B', binascii.unhexlify(startTimeBytes[0:2]))
	hour = struct.unpack('<B', binascii.unhexlify(startTimeBytes[2:4]))
	day = struct.unpack('<B', binascii.unhexlify(startTimeBytes[4:6]))
	second = struct.unpack('<B', binascii.unhexlify(startTimeBytes[6:8]))
	month = struct.unpack('<B', binascii.unhexlify(startTimeBytes[8:10]))
	year = struct.unpack('<B', binascii.unhexlify(startTimeBytes[10:12]))
	print('Start Time: ' + str(hour[0]) + ':' + str(minute[0]) + ':' + str(second[0]))
	print('Start Date: ' + str(month[0]) + '\\' + str(day[0]) + '\\' + str(year[0]))
	logFile.write('Start Time: ' + str(hour[0]) + ':' + str(minute[0]) 
		+ ':' + str(second[0]) + '\n')
	logFile.write('Start Date: ' + str(month[0]) + '\\' + str(day[0]) + '\\' 
		+ str(year[0]) + '\n')

	endTimeBytes = hexBytes[74:86]
	minute = struct.unpack('<B', binascii.unhexlify(endTimeBytes[0:2]))
	hour = struct.unpack('<B', binascii.unhexlify(endTimeBytes[2:4]))
	day = struct.unpack('<B', binascii.unhexlify(endTimeBytes[4:6]))
	second = struct.unpack('<B', binascii.unhexlify(endTimeBytes[6:8]))
	month = struct.unpack('<B', binascii.unhexlify(endTimeBytes[8:10]))
	year = struct.unpack('<B', binascii.unhexlify(endTimeBytes[10:12]))
	print('End Time: ' + str(hour[0]) + ':' + str(minute[0]) + ':' + str(second[0]))
	print('End Date: ' + str(month[0]) + '\\' + str(day[0]) + '\\' + str(year[0]))
	logFile.write('End Time: ' + str(hour[0]) + ':' + str(minute[0]) 
		+ ':' + str(second[0]) + '\n')
	logFile.write('End Date: ' + str(month[0]) + '\\' + str(day[0]) + '\\' 
		+ str(year[0]) + '\n')

	totalizerStartBytes = hexBytes[100:116]
	print(totalizerStartBytes)
	totalizerStart = struct.unpack('<d', binascii.unhexlify(totalizerStartBytes))
	print('Totalizer Start: ' + str(totalizerStart[0]))
	totalizerEndBytes = hexBytes[118:134]
	totalizerEnd = struct.unpack('<d', binascii.unhexlify(totalizerEndBytes))
	print('Totalizer End: ' + str(totalizerEnd[0]))
	grossVolumeBytes = hexBytes[134:150]
	grossVolume = struct.unpack('<d', binascii.unhexlify(grossVolumeBytes))
	print('Gross Volume: ' + str(grossVolume[0]))
	volumeBytes = hexBytes[150:166]
	volume = struct.unpack('<d', binascii.unhexlify(volumeBytes))
	print('Volume: ' + str(volume[0]))

	counter += 1
	time.sleep(2)

curTime = str(datetime.datetime.now().time())
print(curTime)
logFile.write(curTime + '\n')
print(endStr)
logFile.write(endStr + '\n')