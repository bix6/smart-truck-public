#!/usr/bin/env python3

import serial, time

ser = serial.Serial(
	port='/dev/cu.usbserial',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=5
	)

myCmd = bytearray(b'\x7e\x01\xff\x48\x01\x00\x00\xb7\x7e')
goodReplies = 0
badReplies = 0

#Necessary?
ser.reset_input_buffer()
ser.reset_output_buffer()

#50 max
for i in range(0,50):
	print(i)
	print(myCmd.hex())
	ser.write(myCmd)
	#cmdIn = ser.read(size=155)
	myBuffer = bytearray([])
	while True:
		oneByte = ser.read(1)
		#print(oneByte)
		myBuffer += oneByte
		if len(myBuffer) > 10 and oneByte == b'~':
			#print('Exit')
			cmdIn = myBuffer
			break
	print(len(cmdIn))
	print(cmdIn.hex())
	print(cmdIn)
	if cmdIn.startswith(b'~') and cmdIn.endswith(b'~'):
		print('Good Reply')
		goodReplies += 1
	else:
		print('Bad Reply')
		badReplies += 1
	myCmd[5] = myCmd[5] + 1
	myCmd[7] = myCmd[7] - 1
	print()
	time.sleep(.5)

print('Good Replies: ' + str(goodReplies))
print('Bad Replies: ' + str(badReplies))