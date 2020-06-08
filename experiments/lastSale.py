#import time, datetime, serial, struct, requests
import serial, struct

ser = serial.Serial(
	#port='/dev/ttyUSB0',
	port='/dev/cu.usbserial',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=5
	)

curSale = ''
lastSaleSent = ''
curSaleCmd = b'\x7e\x01\xff\x47\x73\x46\x7e'
curTransCmd = bytearray(b'\x7e\x01\xff\x48\x01\x00\x00\xb7\x7e')
myTrans = []
mySales = []

def readIn():
	myBuffer = bytearray([])
	counter=0
	while counter<500:
		oneByte = ser.read(1)
		print(oneByte)
		if oneByte == b'':
			print('Space Cadet')
		myBuffer += oneByte
		if len(myBuffer) > 2 and oneByte == b'~':
			return myBuffer
		counter += 1

ser.write(curSaleCmd)
cmdIn = readIn()
curSale = struct.unpack('<l', cmdIn[5:9])[0]
lastSaleSent = curSale - 50

try:
    f = open('lastSaleSent.txt','r')
    lss = f.readline()
    f.close()

    if lss.isdigit():
        lastSaleSent = int(lss)
except Exception as e:
    print('Warning! No Last Sale Sent', e)
    pass

for i in range(0,curSale - lastSaleSent):
	ser.write(curTransCmd)
	cmdIn = readIn()
	myTrans.append(cmdIn)
	mySales.append(struct.unpack('<l', cmdIn[5:9])[0])
	curTransCmd[5] = curTransCmd[5] + 1
	curTransCmd[7] = curTransCmd[7] - 1

print(list(reversed(myTrans)))
print(list(reversed(mySales)))

