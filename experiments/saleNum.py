#!/usr/bin/env python3

# saleNum.py
# Bix 8/2/18
# Gets the Incremental Sale Number
# TODO: This needs to be validated - I am not sure I am selecting the right bytes
# May also be some conversion issues since the command returned is mismatched to the sent command

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

outF = open('saleNum.txt', 'w')
cmdSaleNum = b'\x7E\x01\xFF\x47\x73\x46\x7E'

print("----------START----------")
print("Writing To Serial... " + cmdSaleNum.hex())
ser.write(cmdSaleNum)
rsp1 = ser.readline()
print("Reading From Serial..." + rsp1.hex())
saleNum = rsp1.hex()[10:18]
revSaleNum = ''
print("Extracted Hex Sale Number..." + saleNum)
for i in range(8,0,-2):
    revSaleNum += saleNum[i-2:i]
print("Extracted Hex Sale Number Reverse..." + revSaleNum)
print("Sale Number... " + str(int(revSaleNum,16)))

outF.write("Command: " + cmdSaleNum.hex() + '\n')
outF.write("Response: " + rsp1.hex() + '\n')
outF.write("Sale Number: " + str(int(revSaleNum,16)) + '\n')

print("Output logged to saleNum.txt...")
print("-----------END-----------")

outF.close()
