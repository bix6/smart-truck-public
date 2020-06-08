#!/usr/bin/env python3

import time
import serial
import os
import sys

ser = serial.Serial(
    #port='COM3',
    #port='/dev/ttyUSB0',
    port='/dev/cu.usbserial',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )

print(os.getcwd())
otptF = open('outputFile.txt', 'w')
print('Serial Name:' + ser.name)

cmdSaleNum = b'\x7E\x01\xFF\x47\x73\x46\x7E'
cmdStart = b'\x7E\x01\xFF\x4F\x01\xB0\x7E'
cmdEnd = b'\x7E\x01\xFF\x4F\x03\xAE\x7E'
cmdLastTrans = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'

ser.write(cmdSaleNum)
rsp1 = bytes([ser.readline()])
print(rsp1)
otptF.write(rsp1)
otptF.write('\n')

ser.write(cmdStart)
rsp2 = bytes([ser.readline()])
print(rsp2)
otptF.write(rsp2)
otptF.write('\n')

print('Start Sleep...')
time.sleep(5)
print('End Sleep...')

ser.write(cmdEnd)
rsp3 = bytes([ser.readline()])
print(rsp3)
otptF.write(rsp3)
otptF.write('\n')

ser.write(cmdLastTrans)
rsp4 = bytes([ser.readline()])
print(rsp4)
otptF.write(rsp4)
otptF.write('\n')
otptF.close()
