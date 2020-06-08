# !/usr/bin/env python3

# binaryTest.py
# Bix 8/7/18
# Binary Tester

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



cmdLastTrans = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'
cmdLastTransName = 'cmdLastTrans'

print(cmdLastTrans)
print(len(cmdLastTrans))
print(cmdLastTrans.hex())
print(b'\x7E') #b'~'
print(b'\x7E'.hex()) #7e
print(b'\x01') #b'\x01'
print(b'\x01'.hex()) #01
print(b'\xFF') #b'\xff'
print(b'\xFF'.hex()) #ff
print(b'\x48') #b'H'
print(b'\x48'.hex()) #48
# bytes object has no attribute unhexlify print(cmdLastTrans.unhexlify())
# bytes object has no attribute unhexlify print(cmdLastTrans.unhexlify().hex())
# str object has no attribute unhexlify print(cmdLastTrans.hex().unhexlify())

ser.write(cmdLastTrans)
textOutBin = cmdLastTransName + ' Bin Out: ' + str(cmdLastTrans)
textOutHex = cmdLastTransName + ' Hex Out: ' + cmdLastTrans.hex()
print(textOutBin)
print(textOutHex)

time.sleep(1.5)
bytesIn = ser.readline()
print(len(bytesIn))
print(len(bytesIn)*2)
textInBin = cmdLastTransName + 'Bin In: ' + str(bytesIn)
textInHex = cmdLastTransName + 'Hex In: ' + bytesIn.hex()
print(textInBin)
print(textInHex)

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
