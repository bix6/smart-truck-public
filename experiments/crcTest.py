#!/usr/bin/env python3

# crcTest.py
# Bix 8/22/18
# crc testarossa

import time, serial, os, sys
from PyCRC.CRC16 import CRC16

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

#outF = open('saleNum.txt', 'w')
cmdSaleNum = b'\x7E\x01\xFF\x47\x73\x46\x7E'

print("Command Bytes: " + str(cmdSaleNum))
print("Command Hex: " + cmdSaleNum.hex())
myCRC = CRC16().calculate(bytes(cmdSaleNum[1:5]))
print(myCRC)
myCRC = CRC16().calculate(bytes(cmdSaleNum[5:6]))
print(myCRC)
myZero = int.from_bytes(b'\x00', byteorder='little')
print(myZero)
myDest = int.from_bytes(cmdSaleNum[1:2], byteorder='little')
print(myDest)
mySource = int.from_bytes(cmdSaleNum[2:3], byteorder='little')
print(mySource)
myMessage = int.from_bytes(cmdSaleNum[3:5], byteorder='little')
print(myMessage)
myCalc = myZero - (myDest + mySource + myMessage)
print(myCalc)

myCalc = myCalc.to_bytes(1, byteorder='little')
print(myCalc)
