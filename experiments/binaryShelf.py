#!/usr/bin/env python3

''' binaryShelf.py
bix 8/15/18
binary shelf testing'''

import shelve

shelfFile = shelve.open('binaryShelfTest')

try:
	print(shelfFile['lastSaleSent'])
except Exception as e:
	shelfFile['lastSaleSent'] = 100

try:
	print(shelfFile['truckID'])
except Exception as e:
	shelfFile['truckID'] = 6

shelfFile.close()