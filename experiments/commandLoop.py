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
    elif cmdOut == cmdLastTrans:
        print('Here - Trans Breakdown')
        rawCmd = cmdIn[10:302] # 146 bytes = 292
        saleBytes = rawCmd[0:8]
        saleNum = struct.unpack('<l', binascii.unhexlify(saleBytes))
        print('Sale Number: ' + str(saleNum[0]))
        #TODO transTypeBytes = rawCmd[8:12]
        print('TODO Transaction Type...')
        #transType = struct.unpack('<p', binascii.unhexlify(transTypeBytes))
        #print(transType[0])
        indexBytes = rawCmd[12:14]
        myIndex = struct.unpack('<b', binascii.unhexlify(indexBytes))
        print('Index: ' + str(myIndex[0]))
        numSummaryRecordsBytes = rawCmd[14:16]
        numSummaryRecords = struct.unpack('<b', binascii.unhexlify(numSummaryRecordsBytes))
        print('# of Summary Records: ' + str(numSummaryRecords[0]))
        numRecordsSummarizedBytes = rawCmd[16:18]
        numRecordsSummarized = struct.unpack('<b', binascii.unhexlify(numRecordsSummarizedBytes))
        print('# of Records Summarized: ' + str(numRecordsSummarized[0]))
        productIDBytes = rawCmd[18:20]
        productID = struct.unpack('<B', binascii.unhexlify(productIDBytes))
        print('Product ID: ' + str(productID[0]))
        #TODO productInfoBytes = rawCmd[20:50]
        print('TODO Product Info...')
        #productInfo = struct.unpack('<p', binascii.unhexlify(productInfoBytes))
        #print('Product Info: ' + str(productInfo[0]))
        productInfoNullTerminationBytes = rawCmd[50:52]
        productInfoNullTermination = struct.unpack('b', binascii.unhexlify(productInfoNullTerminationBytes))
        print('Product Info Null Termination: ' + str(productInfoNullTermination[0]))
        startTimeBytes = rawCmd[52:64]
        minute = struct.unpack('<B', binascii.unhexlify(startTimeBytes[0:2]))
        hour = struct.unpack('<B', binascii.unhexlify(startTimeBytes[2:4]))
        day = struct.unpack('<B', binascii.unhexlify(startTimeBytes[4:6]))
        second = struct.unpack('<B', binascii.unhexlify(startTimeBytes[6:8]))
        month = struct.unpack('<B', binascii.unhexlify(startTimeBytes[8:10]))
        year = struct.unpack('<B', binascii.unhexlify(startTimeBytes[10:12]))
        print('Start: ' + str(hour[0]) + ':' + str(minute[0]) + ':' + str(second[0]) + '...'
              + str(day[0]) + '\\' + str(month[0]) + '\\' + str(year[0]))
        endTimeBytes = rawCmd[64:76]
        minute = struct.unpack('<B', binascii.unhexlify(endTimeBytes[0:2]))
        hour = struct.unpack('<B', binascii.unhexlify(endTimeBytes[2:4]))
        day = struct.unpack('<B', binascii.unhexlify(endTimeBytes[4:6]))
        second = struct.unpack('<B', binascii.unhexlify(endTimeBytes[6:8]))
        month = struct.unpack('<B', binascii.unhexlify(endTimeBytes[8:10]))
        year = struct.unpack('<B', binascii.unhexlify(endTimeBytes[10:12]))
        print('End: ' + str(hour[0]) + ':' + str(minute[0]) + ':' + str(second[0]) + '...'
              + str(day[0]) + '\\' + str(month[0]) + '\\' + str(year[0]))
        tankLoadBytes = rawCmd[76:84]
        tankLoad = struct.unpack('<f', binascii.unhexlify(tankLoadBytes))
        print('Tank Load: ' + str(tankLoad[0]))
        subtotalBytes = rawCmd[84:92]
        subtotal = struct.unpack('<f', binascii.unhexlify(subtotalBytes))
        print('Subtotal: ' + str(subtotal[0]))
        totalizerStartBytes = rawCmd[92:108]
        totalizerStart = struct.unpack('<d', binascii.unhexlify(totalizerStartBytes))
        print('Totalizer Start: ' + str(totalizerStart[0]))
        totalizerEndBytes = rawCmd[108:124]
        totalizerEnd = struct.unpack('<d', binascii.unhexlify(totalizerEndBytes))
        print('Totalizer End: ' + str(totalizerEnd[0]))
        grossVolumeBytes = rawCmd[124:140]
        grossVolume = struct.unpack('<d', binascii.unhexlify(grossVolumeBytes))
        print('Gross Volume: ' + str(grossVolume[0]))
        volumeBytes = rawCmd[140:156]
        volume = struct.unpack('<d', binascii.unhexlify(volumeBytes))
        print('Volume: ' + str(volume[0]))
        avgTempBytes = rawCmd[156:164]
        avgTemp = struct.unpack('<f', binascii.unhexlify(avgTempBytes))
        print('Avg Temp: ' + str(avgTemp[0]))
        unitPriceBytes = rawCmd[164:172]
        unitPrice = struct.unpack('<f', binascii.unhexlify(unitPriceBytes))
        print('Unit Price: ' + str(unitPrice[0]))
        #TODO taxDiscounts = rawCmd[172:244]
        print('TODO Tax Discounts...')
        nonZeroFlowBytes = rawCmd[244:248]
        nonZeroFlow = struct.unpack('<H', binascii.unhexlify(nonZeroFlowBytes))
        print('Non-zero flow (# 0.1s periods with flow >0): ' + str(nonZeroFlow[0]))
        #TODO bitFieldBytes = rawCmd[248:252]
        print('TODO bit field')
        #TODO tankIDBytes = rawCmd[252:272]
        print('TODO tank ID')
        #TODO tankIDNullTermination = rawCmd[272:276]
        print('TODO tank ID null term')
        totalCostBytes = rawCmd[276:292]
        totalCost = struct.unpack('<d', binascii.unhexlify(totalCostBytes))
        print('Cost: ' + str(totalCost[0]))
        #TODO Missing last 2 bytes
        #TODO CRC of entire transaction
        
        
        
startStr = '---START---'
endStr = '---END---'
print(startStr)
outF.write(startStr + '\n')

for i in range(len(cmdsOut)):   
    time.sleep(1.1)
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

# print('Totalizer Change: ' + str(totalizerHolder[1]-totalizerHolder[0]))
print(endStr)
outF.write(endStr + '\n')
outF.close()
