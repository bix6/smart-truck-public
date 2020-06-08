# !/usr/bin/env python3

# binaryTest2.py
# Bix 8/7/18
# Binary Test 2

import time, datetime, serial, os, sys, struct, binascii

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



cmdLastTrans = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'
#cmdLastTransCF = b'\x7E\x01\xFF\x4A\x01\x00\x00\xB5\x7E'
cmdLastTransName = 'cmdLastTrans'

time.sleep(1.5)
ser.write(cmdLastTrans)
textOutBin = cmdLastTransName + ' Bin Out: ' + str(cmdLastTrans)
textOutHex = cmdLastTransName + ' Hex Out: ' + cmdLastTrans.hex()
print(textOutBin)
print(textOutHex)
print('Bytes Out: ' + str(len(cmdLastTrans)))

time.sleep(1.5)
bytesIn = ser.readline()
textInBin = cmdLastTransName + ' Bin In: ' + str(bytesIn)
textInHex = cmdLastTransName + ' Hex In: ' + bytesIn.hex()
print(textInBin)
print(textInHex)
print('Bytes In: ' + str(len(bytesIn)))

print(bytesIn[0:5])
print(bytesIn[0:5].hex())
print(bytesIn[5:9])
print(bytesIn[5:9].hex())
myBytes = bytesIn[5:9].hex()
print(struct.unpack('<l', binascii.unhexlify(myBytes)))
print(struct.unpack('<l', bytesIn[5:9]))

'''
totalizerStartBytes = bytesIn[50:58]
print(totalizerStartBytes)
print(totalizerStartBytes.hex())
totalizerStart = struct.unpack('<d', totalizerStartBytes)
print('Totalizer Start: ' + str(totalizerStart[0]))
'''
