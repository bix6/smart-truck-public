#!/usr/bin/env python3

# transaction.py
# Bix 9/6/18
# transaction module

import struct, logger, datetime, pytz, time, config


class Transaction:
	"""Transaction Class"""

	def __init__(self):
		try:
			self.unit_type = config.get_unit_type()
		except Exception as e:
			logger.log('transaction_init', e)

	def print_attributes_unordered(self):
		try:
			print('\nCustom Transaction Breakdown Unordered')
			my_attr = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self,a))]
			for a in my_attr:
				print(a + ': ' + str(getattr(self, a)))
			print('Breakdown End\n')
		except Exception as e:
			logger.log('transaction_print_attributes_unordered', e)

	def print_attributes(self):
		try:
			print('\nCustom Transaction Breakdown')
			print('command_in: ' + str(self.command_in))
			print('command_in_hex: ' + str(self.command_in_hex))
			print('ticket_num: ' + str(self.ticket_num))
			print('trans_type: ' + str(self.trans_type))
			print('index: ' + str(self.index))
			print('num_sum_records: ' + str(self.num_sum_records))
			print('num_records_summed: ' + str(self.num_records_summed))
			print('product_id: ' + str(self.product_id))
			print('product_info: ' + str(self.product_info))
			print('product_info_null_term: ' + str(self.product_info_null_term))
			print('start_time: ' + str(self.start_time))
			print('end_time: ' + str(self.end_time))
			print('tank_load: ' + str(self.tank_load))
			print('subtotal: ' + str(self.subtotal))
			print('totalizer_start: ' + str(self.totalizer_start))
			print('totalizer_end: ' + str(self.totalizer_end))
			print('gross_volume: ' + str(self.gross_volume))
			print('volume: ' + str(self.volume))
			print('avg_temp: ' + str(self.avg_temp))
			print('unit_price: ' + str(self.unit_price))
			print('TODO_six_tax_fields: ' + str(self.six_tax_fields))
			print('num_non_zero_flow: ' + str(self.num_non_zero_flow))
			print('TODO_bit_field: ' + str(self.bit_field))
			print('tank_id: ' + str(self.tank_id))				
			print('tank_id_null_term: ' + str(self.tank_id_null_term))
			print('total_cost: ' + str(self.total_cost))
			print('custom_field_1: ' + str(self.custom_field_1))
			print('custom_field_2: ' + str(self.custom_field_2))
			print('custom_field_3: ' + str(self.custom_field_3))
			print('custom_field_4: ' + str(self.custom_field_4))
			print('custom_field_5: ' + str(self.custom_field_5))
			print('custom_field_6: ' + str(self.custom_field_6))
			print('custom_field_7: ' + str(self.custom_field_7))
			print('null_termination: ' + str(self.null_termination))
			print('crc: ' + str(self.crc))
			print('Breakdown End\n')
		except Exception as e:
			logger.log('transaction_print_attributes', e)

	def make_payload(self):
		try:
			payload = {}
			payload['transaction_id'] = self.ticket_num
			payload['ticket_number'] = self.ticket_num
			payload['unit_type'] = self.unit_type
			payload['start_time'] = self.start_time.isoformat()
			payload['end_time'] = self.end_time.isoformat()
			payload['units'] = self.volume
			my_data = {}
			my_data['totalizer_start'] = self.totalizer_start
			my_data['totalizer_end'] = self.totalizer_end
			my_data['gross_volume'] = self.gross_volume
			my_data['custom_field_1'] = self.custom_field_1
			my_data['delta_time'] = self.delta_time
			payload['data'] = my_data
			return payload
		except Exception as e:
			logger.log('transaction_make_payload', e)

	def make_payload_zap(self):
		try:
			payload = {}
			payload['ticket_number'] = self.ticket_num
			payload['start_time'] = self.start_time.strftime("%m/%d/%Y %H:%M:%S")
			payload['end_time'] = self.end_time.strftime("%m/%d/%Y %H:%M:%S")
			payload['units'] = self.volume
			payload['delta_time'] = self.delta_time
			return payload
		except Exception as e:
			logger.log('transaction_make_payload_zap', e)

	def make_payload_zap_dump(self):
		try:
			payload = {}
			payload['ticket_number'] = self.ticket_num
			payload['start_time'] = self.start_time.strftime("%m/%d/%Y %H:%M:%S")
			payload['end_time'] = self.end_time.strftime("%m/%d/%Y %H:%M:%S")
			payload['units'] = self.volume
			payload['totalizer_start'] = self.totalizer_start
			payload['totalizer_end'] = self.totalizer_end
			payload['totalizer_units'] = self.totalizer_end - self.totalizer_start
			payload['delta_time'] = self.delta_time
			return payload
		except Exception as e:
			logger.log('transaction_make_payload_zap', e)

	def breakdown_custom_trans(self, cmd_in):
		try:
			self.command_in = cmd_in
			self.command_in_hex = cmd_in.hex()
			self.ticket_num = struct.unpack('<l', cmd_in[5:9])[0]
			self.trans_type = int.from_bytes(cmd_in[9:11], byteorder='little', signed=True)
			self.index = struct.unpack('<b', cmd_in[11:12])[0]
			self.num_sum_records = struct.unpack('<b', cmd_in[12:13])[0]
			self.num_records_summed = struct.unpack('<b', cmd_in[13:14])[0]
			self.product_id = struct.unpack('<B', cmd_in[14:15])[0]
			self.product_info = "".join([chr(c) for c in cmd_in[15:30] if c != 0])
			self.product_info_null_term = struct.unpack('<b', cmd_in[30:31])[0]
			start = [int(struct.unpack('<B', cmd_in[31+i:32+i])[0]) for i in range(0,6)]
			end = [int(struct.unpack('<B', cmd_in[37+i:38+i])[0]) for i in range(0,6)]
			start_dt = datetime.datetime(start[5]+2000,start[4],start[2],start[1],start[0],start[3])
			end_dt = datetime.datetime(end[5]+2000,end[4],end[2],end[1],end[0],end[3])
			local = pytz.timezone(config.get_timezone())
			dst_enabled = False
			if time.localtime().tm_isdst == 1:
				dst_enabled = True
			start_dt_loc = local.localize(start_dt, is_dst=dst_enabled)
			end_dt_loc = local.localize(end_dt, is_dst=dst_enabled)
			self.start_time = start_dt_loc.astimezone(pytz.utc)
			self.end_time = end_dt_loc.astimezone(pytz.utc)
			self.delta_time = (self.end_time-self.start_time).total_seconds()
			self.tank_load = struct.unpack('<f', cmd_in[43:47])[0]
			self.subtotal = struct.unpack('<f', cmd_in[47:51])[0]
			self.totalizer_start = struct.unpack('<d', cmd_in[51:59])[0]
			self.totalizer_end = struct.unpack('<d', cmd_in[59:67])[0]
			self.gross_volume = struct.unpack('<d', cmd_in[67:75])[0]
			self.volume = struct.unpack('<d', cmd_in[75:83])[0]
			self.avg_temp = struct.unpack('<f', cmd_in[83:87])[0]
			self.unit_price = struct.unpack('<f', cmd_in[87:91])[0]
			#TODO six tax fields
			self.six_tax_fields = cmd_in[91:127]
			self.num_non_zero_flow = struct.unpack('<H', cmd_in[127:129])[0]
			#TODO bit field
			self.bit_field = cmd_in[129:131]
			self.tank_id = "".join([chr(c) for c in cmd_in[131:141] if c != 0])				
			self.tank_id_null_term = int.from_bytes(cmd_in[141:143], byteorder='little', signed=True)
			self.total_cost = struct.unpack('<d', cmd_in[143:151])[0]
			self.custom_field_1 = "".join([chr(c) for c in cmd_in[151:165] if c != 0])		
			self.custom_field_2 = "".join([chr(c) for c in cmd_in[165:179] if c != 0])
			self.custom_field_3 = "".join([chr(c) for c in cmd_in[179:188] if c != 0])
			self.custom_field_4 = "".join([chr(c) for c in cmd_in[188:195] if c != 0])
			self.custom_field_5 = "".join([chr(c) for c in cmd_in[195:202] if c != 0])
			self.custom_field_6 = "".join([chr(c) for c in cmd_in[202:209] if c != 0])
			self.custom_field_7 = "".join([chr(c) for c in cmd_in[209:216] if c != 0])
			self.null_termination = struct.unpack('<b', cmd_in[216:217])[0]
			self.crc = struct.unpack('<H', cmd_in[217:219])[0]			
			return self
		except Exception as e:
			logger.log('transaction_breakdown_custom_trans', e)