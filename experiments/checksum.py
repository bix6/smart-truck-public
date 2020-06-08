#!/usr/bin/env python3

# checksum.py
# Bix 9/4/18
# Checksum tests

my_bytes = b'\x7e\x01\xff\x53\x70\x00\x3d\x7e'
my_bytes2 = b'\x7e\x01\xff\x47\x70\x49\x7e'
my_bytes3 = b'\x7e\xff\x01\x46\x70\x00\x4a\x7e'

my_bytes_sum = 0-sum(my_bytes[1:len(my_bytes)-2])
my_bytes2_sum = 0-sum(my_bytes2[1:len(my_bytes2)-2])
my_bytes3_sum = 0-sum(my_bytes3[1:len(my_bytes3)-2])

print(hex(my_bytes_sum % 256))
print(hex(my_bytes2_sum % 256))
print(hex(my_bytes3_sum % 256))




print('\n\n')
char_forbidden = 126 #b'\x7e' is ~
char_escape = 125 #b'\x7d' is }
#char_escape = b'\x7d'
char_control = 32 #b'\x20' is 
#char_escape = b'\x20'

#bytes_my = bytearray(b'\x7e\x01\xff\x7e\x7e')
#bytes_my = bytearray(b'\x7e\x01\xff\x7e\x7e\x7e')
#bytes_my = bytearray(b'\x7e\x01\xff\x7e\x7e\x7d\x7e')
#bytes_my = bytearray(b'\x7e\x01\xff\x7d\x7e')
#bytes_my = bytearray(b'\x7e\x01\xff\x7d\x77\x7d\x7e')
#bytes_my = bytearray(b'\x7e\x01\xff\x7d\x7e\x77\x7d\x7e')
bytes_my = bytearray(b'\x7e\x01\xff\x7d\x7e\x77\x7d\x7e\x87\x7e\x7d\x7e')

print(bytes_my)
bytes_my_mid = bytes_my[1:- 1]
bytes_needs_escape = [(i,j) for i,j in enumerate(bytes_my_mid) if j==char_forbidden or j==char_escape]
for i, j in bytes_needs_escape[::-1]:
	bytes_my[i+1] = j^char_control #i+1 since 1st byte is excluded in enum
	bytes_my.insert(i+1, char_escape)
print(bytes_my)

bytes_my_mid = bytes_my[1:- 1]
bytes_needs_escape = [(i,j) for i,j in enumerate(bytes_my_mid) if j==char_escape]
for i, j in bytes_needs_escape[::-1]:
	bytes_my[i+2] = bytes_my[i+2]^char_control #i+2 since 1st byte excluded in enum and i+1 is escape char
	del bytes_my[i+1]
print(bytes_my)
