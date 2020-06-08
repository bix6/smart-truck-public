#!/usr/bin/env python3

'''poc5.py
Bix 8/14/18
Proof of Concept V5
Send timestamps, ticket num and volume to cloud
V5: loop with connection testing, all missed trans, logging

To run on RasPi switch port to /dev/ttyUSB0'''

import time, datetime, serial, struct, requests

ser = serial.Serial(
	#port='/dev/ttyUSB0',
	port='/dev/cu.usbserial',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=5
	)

sleepTime = 10
dummyVal = 6
truckID = dummyVal
curSaleCmd = b'\x7e\x01\xff\x47\x73\x46\x7e'
cmdOut = bytearray(b'\x7e\x01\xff\x48\x01\x00\x00\xb7\x7e')
emrStateCmd = b'\x7e\x01\xff\x54\x08\xa4\x7e'
lastSaleSent = -1
myTrans = []
noConnectionCounter = 0
payload = {
    'start_time': datetime.datetime.utcnow().isoformat(),
    'end_time': datetime.datetime.utcnow().isoformat(),
    'units': dummyVal,
    'unit_type': 'gas',
    'latitude': dummyVal,
    'longitude': dummyVal,
    'truckId': truckID,
    'transaction_id': dummyVal
}

def readIn():
	myBuffer = bytearray([])
	for i in range(0,500):
		oneByte = ser.read(1)
		myBuffer += oneByte
		if oneByte == b'':
			return oneByte
		if len(myBuffer) > 2 and oneByte == b'~':
			return myBuffer

def logData(keyIn, valIn):
	f = open('pocLog.txt', 'a')
	f.write(str(keyIn) + ': ' + str(valIn) + '\n')
	f.close()

def getLastSaleSent(curSaleLoc):
	try:
		f = open('lastSaleSent.txt','r')
		lss = f.readline()
		f.close()

		if lss.isdigit():
			return int(lss)
	except Exception as e:
		logData('no_last_sale', 'true')
		return curSaleLoc - 50

def getTruckID():
		try:
			# This path will change to /boot/truckId on the Pi
			#f = open('/boot/truckId','r')
			f = open('truckID.txt','r')
			tid = f.readline()
			f.close()

			if tid.isdigit():
				return tid
		except Exception as e:
			logData('no_truck_id', 'true')
			return dummyVal

logData('NEWLOOP', 'INITIATED')
logData('pi_start', datetime.datetime.utcnow().isoformat())
truckID = getTruckID()
payload['truckId'] = truckID
#url = 'http://httpbin.org/post'
url = f"filld/trucks/api/v1/trucks/{truckID}/delivery"
while True:
	ser.write(curSaleCmd)
	cmdIn = readIn()
	if cmdIn == b'':
		noConnectionCounter += 1
	else:
		ser.write(emrStateCmd)
		emrStatus = readIn()
		if int(emrStatus[5:6].hex()) != 2:
			print('not in delivery mode')
			curSale = struct.unpack('<l', cmdIn[5:9])[0]
			if lastSaleSent == -1:
				lastSaleSent = getLastSaleSent(curSale)

			# get transactions
			for i in range(0, curSale - lastSaleSent):
				ser.write(cmdOut)
				cmdIn = readIn()
				myTrans.append(cmdIn)
				cmdOut[5] = cmdOut[5] + 1
				cmdOut[7] = cmdOut[7] - 1
			myTrans = list(reversed(myTrans))


			# transaction breakdown
			for t in myTrans:
				cmdIn = t
				payload['transaction_id'] = struct.unpack('<l', cmdIn[5:9])[0]

				sStart, sEnd = [],[]
				for i in range (0, 6):
					sStart.append(str(struct.unpack('<B', cmdIn[31+i:32+i])[0]))
					sEnd.append(str(struct.unpack('<B', cmdIn[37+i:38+i])[0]))
				sStartStr = sStart[5]+'-'+sStart[4]+'-'+sStart[2]+'T'+sStart[1]+':'+sStart[0]+':'+sStart[3]
				payload['start_time'] = sStartStr
				sEndStr = sEnd[5]+'-'+sEnd[4]+'-'+sEnd[2]+'T'+sEnd[1]+':'+sEnd[0]+':'+sEnd[3]
				payload['end_time'] = sEndStr

				payload['units'] = struct.unpack('<d', cmdIn[75:83])[0]

				r = requests.post(url, json=payload, headers={'Authorization':'Basic token'})

				if r.status_code == requests.codes.ok:
				    print(r.text)
				    pass
				else:
					logData('post_error', r.raise_for_status())

				time.sleep(.1)

			# Update last sale
			if lastSaleSent != curSale:
				lastSaleSent = curSale
				f = open('lastSaleSent.txt','w')
				f.write(str(lastSaleSent))
				f.close()

			# Reset Vars
			cmdOut = bytearray(b'\x7e\x01\xff\x48\x01\x00\x00\xb7\x7e')
			myTrans = []
			noConnectionCounter = 0
			payload = {
			    'start_time': datetime.datetime.utcnow().isoformat(),
			    'end_time': datetime.datetime.utcnow().isoformat(),
			    'units': dummyVal,
			    'unit_type': 'gas',
			    'latitude': dummyVal,
			    'longitude': dummyVal,
			    'truckId': truckID,
			    'transaction_id': dummyVal
			}

	if noConnectionCounter != 0:
		logData('no_connection_counter', noConnectionCounter)
	logData('loop_end', datetime.datetime.utcnow().isoformat())
	time.sleep(sleepTime)
	print('loop complete')

# need to break loop to get here
logData('pi_end', datetime.datetime.utcnow().isoformat())
logData('SELF-DESTRUCT', 'COMPLETE')

