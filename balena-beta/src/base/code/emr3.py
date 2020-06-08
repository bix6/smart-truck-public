#!/usr/bin/env python3

# emr3.py
# Bix 8/28/18
# emr3 Module

import serial, logger, struct, binascii, transaction, os, config, time

class EMR3:
	"""EMR3 Class"""

	CMD_SERIAL_NUM = b'\x7e\x01\xff\x47\x72\x47\x7e' #G,r
	CMD_CUSTOM_TRANS_START = b'\x7e\x01\xff\x4a\x01\x00\x00\xb5\x7e' #J,01,0,0
	CMD_EMR_STATE = b'\x7e\x01\xff\x54\x08\xa4\x7e' #T,8
	CMD_METER_STATUS = b'\x7e\x01\xff\x54\x01\xab\x7e' #T,1
	CMD_GET_REGISTER_CONFIG = b'\x7e\x01\xff\x45\x17\xa4\x7e' #E, 23
	CMD_SET_REGISTER_CONFIG = b'' # TODO
	CMD_CUR_SALE = b'\x7e\x01\xff\x47\x73\x46\x7e' #G, s
	CMD_START_METER = b'\x7e\x01\xff\x4f\x01\xb0\x7e' #O, 1
	CMD_REAL_TIME_TOTALIZER = b'\x7e\x01\xff\x47\x4c\x6d\x7e' #G, L

	DELAY_TIME = 1

	def __init__(self):
		try:
			if os.uname()[4].startswith("arm"):
				self.ser = serial.Serial(
					port='/dev/ttyUSB0', #RasPi
					baudrate=9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS,
					timeout=1
					)
			else: 
				self.ser = serial.Serial(
					port='/dev/cu.usbserial', # Mac
					#port='COM3', # PC
					baudrate=9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS,
					timeout=1
					)
			self.connected = False
			self.serial_num = None
			self.new_trans = False
			self.last_emr_state = -1
		except Exception as e:
			logger.log('emr3_init', e)

	def escape_bytes(self, cmd_in):
		try:
			char_escape = 125 #b'\x7d' is }
			char_control = 32 #b'\x20' is 
			bytes_mid = cmd_in[1:-1]
			bytes_to_remove = [(i,j) for i,j in enumerate(bytes_mid) if j==char_escape]
			for i, j in bytes_to_remove[::-1]:
				cmd_in[i+2] = cmd_in[i+2]^char_control #i+2 since 1st byte excluded in enum and i+1 is escape char
				del cmd_in[i+1]
			return cmd_in
		except Exception as e:
			logger.log('emr3_escape_bytes', e)

	def check_cmd(self, cmd_in):
		try:
			cmd_in = self.escape_bytes(cmd_in)
			checksum_calc = (0 - sum(cmd_in[1:-2])) % 256
			checksum_in = int.from_bytes(cmd_in[-2:-1], byteorder='little', signed=False)
			if checksum_calc == checksum_in:
				return cmd_in
			else:
				logger.log('emr3_check_cmd_fail', cmd_in)
				return None
		except Exception as e:
			logger.log('emr3_check_cmd', e)

	def receive_cmd(self):
		try:
			my_buffer = bytearray()
			for i in range(0,500): # 500 is arbitrary, longest cmd_in is 214 bytes?
				one_byte = self.ser.read(1)
				my_buffer += one_byte
				#print('one_byte', one_byte)
				if one_byte == b'':
					return None
				elif len(my_buffer) > 2 and one_byte == b'~':
					#print('\nreceived:', my_buffer)
					return self.check_cmd(my_buffer)
			logger.log('emr3_receive_cmd', '500 loops exceeded')
			return None
		except Exception as e:
			logger.log('emr3_receive_cmd', e)

	def send_cmd(self, cmd_to_send):
		try:
			self.ser.reset_output_buffer()
			self.ser.reset_input_buffer()
			self.ser.write(cmd_to_send)
			#print('\nsent:', cmd_to_send)
			return self.receive_cmd()
		except Exception as e:
			logger.log('emr3_send_cmd', e)

	def get_emr_state(self):
		try:
			cmd_in = self.send_cmd(self.CMD_EMR_STATE)
			if cmd_in == None:
				self.connected = False
			else:
				self.connected = True
				self.cur_emr_state = int(cmd_in[5:6].hex())
				while self.cur_emr_state == 2:
					print('in delivery mode')
					self.last_emr_state = self.cur_emr_state
					time.sleep(self.DELAY_TIME)
					self.cur_emr_state = self.get_emr_state()
				if self.last_emr_state == 2 and self.cur_emr_state != 2:
					print('delivery completed')
					self.last_emr_state = self.cur_emr_state
					self.new_trans = True

		except Exception as e:
			logger.log('emr3_check_connection', e)

	def get_serial_num(self):
		try:
			cmd_in = self.send_cmd(self.CMD_SERIAL_NUM)
			if cmd_in != None:
				serial_in = "".join([chr(b) for b in cmd_in[5:25] if b != 0])
				if serial_in != "«~": # avoids bad serial on startup
					self.serial_num = serial_in
					logger.log('emr3_get_serial_num', self.serial_num)
			else:
				logger.log('emr3_get_serial_num_bad_cmd_in', cmd_in)
		except Exception as e:
			logger.log('emr3_get_serial_num', e)

	def check_crc(self, cmd_in):
		try:
			crc_in = int.from_bytes(cmd_in[-4:-2], byteorder='little', signed=False)
			bytes_trans = cmd_in[5:-4] # -4 to excl crc
			crc = binascii.crc_hqx(bytes_trans, 0xffff)
			if (crc_in == crc):
				return True
			else:
				return False

		except Exception as e:
			logger.log('emr3_check_crc', e)

	def get_trans(self, cmd_trans=CMD_CUSTOM_TRANS_START):
		try:
			cmd_in = self.send_cmd(cmd_trans)
			if cmd_in != None:
				if self.check_crc(cmd_in):
					self.new_trans = False
					t = transaction.Transaction()
					return t.breakdown_custom_trans(cmd_in)
				else:
					logger.log('emr3_get_trans_crc_fail', cmd_in)
					return None
			else:
				logger.log('emr3_get_trans_bad_cmd', cmd_in)
				return None
		except Exception as e:
			logger.log('emr3_get_trans', e)

	def get_multi_trans(self, TESTING):
		try:
			#TODO lockout meter
			last_sale_sent = config.get_last_sale_sent()
			if last_sale_sent == -1:
				cmd_in = self.send_cmd(self.CMD_CUR_SALE)
				last_sale_sent = str(struct.unpack('<l', cmd_in[5:9])[0])
				config.set_last_sale_sent(last_sale_sent)
			else:
				cmd_in = self.send_cmd(self.CMD_CUR_SALE)
				cur_sale = struct.unpack('<l', cmd_in[5:9])[0]
				if cur_sale > last_sale_sent:
					cmd_trans = bytearray(self.CMD_CUSTOM_TRANS_START)
					my_trans = []
					for i in range(0, cur_sale - last_sale_sent):
						cmd_trans[5] = cmd_trans[5] + 1
						cmd_trans[7] = cmd_trans[7] - 1
						my_trans.insert(0, self.get_trans(cmd_trans))
					for t in my_trans:
						t.breakdown_custom_trans
						payload = t.make_payload_zap_dump()
						if not TESTING:
							logger.log_transaction_zap_dump(payload)
						print(payload)
						time.sleep(self.DELAY_TIME)
					config.set_last_sale_sent(str(cur_sale))
		except Exception as e:
			logger.log('emr3_get_multi_trans', e)

	def start_meter(self):
		try:
			cmd_in = self.send_cmd(self.CMD_START_METER)
			if cmd_in == b'\x7e\xff\x01\x41\x00\xbf\x7e':
				print('Meter started')
				return True
			else:
				print('Meter not started')
				return False

		except Exception as e:
			print('emr3_start_meter', e)
			
	def get_real_time_totalizer(self):
		try:
			cmd_in = self.send_cmd(self.CMD_REAL_TIME_TOTALIZER)
			if cmd_in == None:
				print('EMR not connected')
			else:
				return struct.unpack('<d', cmd_in[5:13])[0]
		except Exception as e:
			print('emr3_get_real_time_totalizer', e)