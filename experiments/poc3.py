# !/usr/bin/env python3

# poc3.py
# Bix 8/8/18
# Proof of Concept 3
# Send timestamps, ticket num and volume to cloud

# To run without EMR3
# Comment out ser block (''')
# Comment out ser.write(cmdOut) (#)
# Comment out cmdIn = ser.readline() (#)
# Remove # from #cmdIn = dummyCmdIn

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

#Most recent trans, random trans, random trans
#cmdOut = b'\x7E\x01\xFF\x48\x01\x00\x00\xB7\x7E'
#cmdOut = b'\x7e\x01\xff\x48\x01\x2e\x00\x89\x7e'
cmdOut = b'\x7e\x01\xff\x48\x01\x1a\x00\x9d\x7e'
dummyCmdIn = b"~\xff\x01I\x03\xa1'\x00\x00\x00\x00\x00\x00\x00\x00GASOLINE\x00\x00\x00\x00\x00\x00\x00\x007\t\x069\x08\x128\t\x06\x01\x08\x12\x00\x00\x00\x00\x00\x00\x00\x0033333\x0bs@\xcd\xcc\xcc\xcc\xcc\xc4s@333333'@333333'@\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00#\x00\xb1\x00TANK 1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xef\x05\xfb~"

counter = 0
CounterMax = 1

while counter < CounterMax:
	payload = {}

	payload['Pi Start'] = datetime.datetime.utcnow().isoformat()
	ser.write(cmdOut)
	payload['Command Out'] = str(cmdOut)
	cmdIn = ser.readline()
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

	counter += 1
	time.sleep(1)

url = 'http://httpbin.org/post'
r = requests.post(url, json=payload)

if r.status_code == requests.codes.ok:
    print(r.text)
else:
    print(r.raise_for_status())
