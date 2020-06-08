# !/usr/bin/env python3

# poc4.py
# Bix 8/13/18
# Proof of Concept V4
# Send timestamps, ticket num and volume to cloud
# V4: loop with connection testing and all trans

# TODO UPDATE To run without EMR3
# Comment out ser block (''')
# Comment out ser.write(cmdOut) (#)
# Comment out while True loop (''')
# Remove # from #cmdIn = dummyCmdIn

# To run on RasPi
# Switch port to /dev/ttyUSB0

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

# Set a default in case the file is missing / corrupt.
truckId = -1
url = 'http://httpbin.org/post'
#url = 'filld/api/v1/trucks/{truckId}/delivery'
#cmdOut = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'
cmdOut = bytearray(b'\x7e\x01\xff\x48\x01\x00\x00\xb7\x7e')
dummyCmdIn = b"~\xff\x01I\x03\xa1'\x00\x00\x00\x00\x00\x00\x00\x00GASOLINE\x00\x00\x00\x00\x00\x00\x00\x007\t\x069\x08\x128\t\x06\x01\x08\x12\x00\x00\x00\x00\x00\x00\x00\x0033333\x0bs@\xcd\xcc\xcc\xcc\xcc\xc4s@333333'@333333'@\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00#\x00\xb1\x00TANK 1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xef\x05\xfb~"
curSaleCmd = b'\x7e\x01\xff\x47\x73\x46\x7e'
payload = {'No Connection':0}
lastSaleSent = 0
myTrans = []
mySales = []

def readIn():
	myBuffer = bytearray([])
	counter=0
	while counter<500:
		oneByte = ser.read(1)
		myBuffer += oneByte
		if oneByte == b'':
			return oneByte
		if len(myBuffer) > 2 and oneByte == b'~':
			return myBuffer
		counter += 1

def getLastSaleSent():
	try:
		f = open('lastSaleSent.txt','r')
		lss = f.readline()
		f.close()

		if lss.isdigit():
			return int(lss)
	except Exception as e:
		print('Warning! No Last Sale Sent', e)
		return - 1

def resetVars():
	cmdOut = bytearray(b'\x7e\x01\xff\x48\x01\x00\x00\xb7\x7e')
	myTrans = []
	mySales = []
	payload = {'No Connection':0}


# Start
payload['Pi Start'] = datetime.datetime.utcnow().isoformat()
time.sleep(1)
while True:
	ser.write(curSaleCmd)
	cmdIn = readIn()
	if cmdIn == b'':
		payload['No Connection'] += 1
	else:
		curSale = struct.unpack('<l', cmdIn[5:9])[0]
		lastSaleSent = getLastSaleSent()
		if lastSaleSent == - 1:
			lastSaleSent = curSale - 50

		for i in range(0, curSale - lastSaleSent):
			ser.write(cmdOut)
			cmdIn = readIn()
			myTrans.append(cmdIn)
			mySales.append(struct.unpack('<l', cmdIn[5:9])[0])
			cmdOut[5] = cmdOut[5] + 1
			cmdOut[7] = cmdOut[7] - 1
			print(mySales)

		myTrans = list(reversed(myTrans))
		mySales = list(reversed(mySales))
		print(mySales)

		for i in myTrans:
			cmdIn = i
			#cmdIn = dummyCmdIn
			payload['Command In'] = str(cmdIn)
			payload['Sale Number'] = struct.unpack('<l', cmdIn[5:9])[0]

			sStart, sEnd = [],[]
			for i in range (0, 6):
				sStart.append(str(struct.unpack('<B', cmdIn[31+i:32+i])[0]))
				sEnd.append(str(struct.unpack('<B', cmdIn[37+i:38+i])[0]))
			sStartStr = sStart[5]+'-'+sStart[4]+'-'+sStart[2]+'T'+sStart[1]+':'+sStart[0]+':'+sStart[3]
			payload['Sale Start'] = sStartStr
			sEndStr = sEnd[5]+'-'+sEnd[4]+'-'+sEnd[2]+'T'+sEnd[1]+':'+sEnd[0]+':'+sEnd[3]
			payload['Sale End'] = sEndStr

			tBytes = [cmdIn[51:59], cmdIn[59:67], cmdIn[67:75], cmdIn[75:83]]
			tNames = ['Totalizer Start', 'Totalizer End', 'Gross Volume', 'Volume']
			for i in range(0,4):
				payload[tNames[i]] = struct.unpack('<d', tBytes[i])[0]

			payload['Pi End'] = datetime.datetime.utcnow().isoformat()

			for k,v in payload.items():
				print('Key: ' + k + ' Value: ' + str(v))
				
			time.sleep(1)
		
		resetVars()

	time.sleep(5)
	print('\n\n\n\n\n\n\n\n')
