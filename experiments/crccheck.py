#!/usr/bin/env python3

# crccheck.py
# Bix 9/6/18
# crccheck

from PyCRC.CRC16 import CRC16
from PyCRC.CRC16DNP import CRC16DNP
from PyCRC.CRC16Kermit import CRC16Kermit
from PyCRC.CRC16SICK import CRC16SICK
from PyCRC.CRCCCITT import CRCCCITT
import binascii 



my_input = b'\x01\x02\x03\x04\x05'
print('my_input')
print(my_input)
crc1 = binascii.crc_hqx(my_input, 0xffff)
print('crc1')
print(crc1)
print('crc1_hex')
print(hex(crc1))