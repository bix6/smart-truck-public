#!/usr/bin/env python3

import serial, struct

ser = serial.Serial(
	port='/dev/cu.usbserial',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=5
	)

#myCmd=b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'
#myCmd = b'\x7e\x01\xff\x47\x64\x55\x7e'
#myCmd = b'\x7e\x01\xff\x48\x01\x2e\x00\x89\x7e'
myCmd = b'\x7e\x01\xff\x48\x01\x1a\x00\x9d\x7e'
myCmd = b'\x7e\x01\xff\x54\x08\xa4\x7e'

#cmdDate = b'\x7e\x01\xff\x47\x64\x55\x7e'
#cmdTime = b'\x7e\x01\xff\x47\x69\x50\x7e'
#cmdSaleNum = b'\x7E\x01\xFF\x47\x73\x46\x7E'
#cmdGrossTotalizer = b'\x7e\x01\xff\x47\x6a\x4f\x7e'
#cmdStart = b'\x7E\x01\xFF\x4F\x01\xB0\x7E'
#cmdEnd = b'\x7E\x01\xFF\x4F\x03\xAE\x7E'
#cmdLastTrans = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'

ser.write(myCmd)
bytesIn = ser.readline()
print(bytesIn)
print(bytesIn.hex())
print(bytesIn[5:6])
print(bytesIn[5:6].hex())