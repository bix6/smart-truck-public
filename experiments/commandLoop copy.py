#!/usr/bin/env python3

# commandLoop.py
# Bix 8/3/18
# Loops through an array of commands and outputs the results to console & CSV

import time
import serial
import os
import sys
import struct
import binascii

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

outF = open('commandLoop.txt', 'a')
cmdDate = b'\x7e\x01\xff\x47\x64\x55\x7e'
cmdTime = b'\x7e\x01\xff\x47\x69\x50\x7e'
cmdSaleNum = b'\x7E\x01\xFF\x47\x73\x46\x7E'
cmdGrossTotalizer = b'\x7e\x01\xff\x47\x6a\x4f\x7e'
cmdStart = b'\x7E\x01\xFF\x4F\x01\xB0\x7E'
cmdEnd = b'\x7E\x01\xFF\x4F\x03\xAE\x7E'
cmdLastTrans = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'
cmdsNames = ['cmdDate', 'cmdTime', 'cmdSaleNum', 'cmdGrossTotalizer', 'cmdStart','cmdEnd',
             'cmdGrossTotalizer', 'cmdLastTrans']
cmdsOut = [cmdDate, cmdTime, cmdSaleNum, cmdGrossTotalizer, cmdStart, cmdEnd,
           cmdGrossTotalizer, cmdLastTrans]
cmdsIn = []

totalizerHolder = []

def inputDecoder(cmdOut, cmdIn):
    if cmdOut == cmdDate:
        rawCmd = cmdIn[10:18]
        century = int(rawCmd[0:2], 16)
        year = int(rawCmd[2:4], 16)
        month = int(rawCmd[4:6], 16)
        day = int(rawCmd[6:8], 16)
        return(str(day) + '\\' +  str(month) + '\\' + str(century) + str(year))
    elif cmdOut == cmdTime:
        rawCmd = cmdIn[10:16]
        hour = int(rawCmd[0:2], 16)
        minutes = int(rawCmd[2:4], 16)
        seconds = int(rawCmd[4:6], 16)
        return(str(hour) + ':' + str(minutes) + ':' + str(seconds))
    elif cmdOut == cmdSaleNum:
        rawCmd = cmdIn[10:18]
        saleNum = struct.unpack('<L', binascii.unhexlify(rawCmd))
        return saleNum[0]
    elif cmdOut == cmdStart or cmdOut == cmdEnd:
        rawCmd = cmdIn
        if rawCmd == '7eff014100bf7e':
            return 'ACK'
        else:
            return 'NACK'
    elif cmdOut == cmdGrossTotalizer:
        rawCmd = cmdIn[10:26]
        grossTotalizer = struct.unpack('<d', binascii.unhexlify(rawCmd))
        totalizerHolder.append(grossTotalizer[0])
        return grossTotalizer[0]

            
        
startStr = '---START---'
endStr = '---END---'
print(startStr)
outF.write(startStr + '\n')

for i in range(len(cmdsOut)):   
    time.sleep(1)
    cmdOut = cmdsOut[i]
    cmdName = cmdsNames[i]
    
    ser.write(cmdOut)
    textOut = cmdName + ' Out: ' + cmdOut.hex()
    print(textOut)
    outF.write(textOut + '\n')
    
    bytesIn = ser.readline()
    cmdsIn.append(bytesIn)
    textIn = cmdName + ' In: ' + bytesIn.hex()
    print(textIn)
    outF.write(textIn + '\n')

    if cmdOut == cmdStart:
        time.sleep(5)

    decodedStr = inputDecoder(cmdOut, bytesIn.hex())
    if decodedStr:
        decodedStr = cmdName + ' Val: ' + str(decodedStr)
        print(decodedStr)
        outF.write(decodedStr + '\n')

print('Totalizer Change: ' + str(totalizerHolder[1]-totalizerHolder[0]))
print(endStr)
outF.write(endStr + '\n')
outF.close()
