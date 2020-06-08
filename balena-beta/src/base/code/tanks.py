#!/usr/bin/env python3

# tanks.py
# Bix 10/4/18
# wii tanks module

import logger, config, os

if os.uname()[4].startswith("arm"):
	import RPi.GPIO as GPIO

class Tanks:
	"""Tanks Class"""

	def __init__(self):
		try:
			self.SPICLK = 18
			self.SPIMISO = 23
			self.SPIMOSI = 24
			self.SPICS = 25

			self.TANK_ADC = [i for i in range(config.get_num_tanks())]

			GPIO.setmode(GPIO.BCM)

			GPIO.setup(self.SPIMOSI, GPIO.OUT)
			GPIO.setup(self.SPIMISO, GPIO.IN)
			GPIO.setup(self.SPICLK, GPIO.OUT)
			GPIO.setup(self.SPICS, GPIO.OUT)

			self.resistance_values = [-1 for i in self.TANK_ADC]
			self.lookup = [config.get_lookup_table(i) for i in self.TANK_ADC]
			self.tank_levels = [config.get_tank_level(i) for i in self.TANK_ADC]
			print(self.tank_levels)
			for i in self.TANK_ADC:
				if self.tank_levels[i] < 0:
					self.tank_levels[i] = self.read_tank_level(i)
				else:
					self.resistance_values[i] = self.read_adc(i)
			print(self.tank_levels)
			for i in self.TANK_ADC:
				config.update_tank_level(i, self.tank_levels[i])
			self.send_payload()
		except Exception as e:
			logger.log('tanks_init', e)

	def read_adc(self, adcnum):
		try:
			clockpin = self.SPICLK
			mosipin = self.SPIMOSI
			misopin = self.SPIMISO
			cspin = self.SPICS

			if ((adcnum > 7) or (adcnum < 0)):
				return -1
			GPIO.output(cspin, True)

			GPIO.output(clockpin, False) # start clock low
			GPIO.output(cspin, False) # bring CS low

			commandout = adcnum
			commandout |= 0x18 # start bit + single-ended bit
			commandout <<= 3 # we only need to send 5 bits here
			for i in range(5):
				if (commandout & 0x80):
					GPIO.output(mosipin, True)
				else:
					GPIO.output(mosipin, False)
				commandout <<= 1
				GPIO.output(clockpin, True)
				GPIO.output(clockpin, False)

			adcout = 0
			# read in one empty bit, one null bit and 10 ADC bits
			for i in range(12):
				GPIO.output(clockpin, True)
				GPIO.output(clockpin, False)
				adcout <<= 1
				if (GPIO.input(misopin)):
					adcout |= 0x1

			GPIO.output(cspin, True)

			adcout >>= 1 # first bit is 'null' so drop it
			return adcout
		except Exception as e:
			logger.log('tanks_read_adc', e)

	def convert_res_to_gal(self, res_in, adc_in):
		try:
			res_high = 1100
			res_low = -1
			gals = 0
			print('adc_in', adc_in, 'res_in', res_in)
			for k in self.lookup[adc_in].keys():
				k = int(k)
				if k > res_low and k < res_in:
					res_low = k
				if k < res_high and k > res_in:
					res_high = k
			print('res_low', res_low, 'res_high', res_high)
			diff = res_high - res_low
			print('diff', diff)
			gal_low = float(self.lookup[adc_in].get(str(res_low), -100))
			gal_high = float(self.lookup[adc_in].get(str(res_high), -10))
			gal_diff = abs(gal_low - gal_high)
			print('gal_low', gal_low, 'gal_high', gal_high)
			if abs(res_low - res_in) < abs(res_high - res_in):
				diff_res_low = abs(res_in - res_low)
				diff_frac = diff_res_low / diff
				print('diff_frac', diff_frac)
				gals = gal_low - gal_diff * diff_frac
				print('gals_l', gals)
			else:
				diff_res_high = abs(res_in - res_high)
				diff_frac = diff_res_high / diff
				print('diff_frac', diff_frac)
				gals = gal_high + gal_diff * diff_frac
				print('gals_h', gals)
			return gals
		except Exception as e:
			logger.log('tanks_convert_res_to_gal', e)

	def read_tank_level(self, adc_in):
		try:
			res = self.read_adc(adc_in)
			self.resistance_values[adc_in] = res
			return self.convert_res_to_gal(res, adc_in)
		except Exception as e:
			logger.log('tanks_read_tank_level', e)

	def update_tank_from_transaction(self, gas_amt):
		try:
			print('\n\nUPDATING TANK')
			print(self.tank_levels)
			res = [self.read_adc(i) for i in self.TANK_ADC]
			max_change = -1
			adc_num = 0 # default to tank 0
			for i in self.TANK_ADC:
				change = res[i] - self.resistance_values[i]
				if change > max_change:
					max_change = change
					adc_num = i
			self.resistance_values[adc_num] = res[adc_num]
			self.tank_levels[adc_num] = self.tank_levels[adc_num] - gas_amt
			print('DONE UPDATING')
			print(self.tank_levels)
			config.update_tank_level(adc_num, self.tank_levels[adc_num])
			self.send_payload()
		except Exception as e:
			logger.log('tanks_update_tank_from_transaction', e)

	def update_tank_levels(self):
		try:
			print('\nSTART UPDATE2')
			print(self.tank_levels)
			for i in self.TANK_ADC:
				res = self.read_adc(i)
				old_level = self.tank_levels[i]
				self.tank_levels[i] = self.convert_res_to_gal(res, i)
				if abs(old_level - self.tank_levels[i]) > 10:
					print('\nChange > 10\n')
			print('END UPDATE2')
			print(self.tank_levels)
			self.send_payload()
		except Exception as e:
			logger.log('tanks_update_tank_levels',)

	def send_payload(self):
		try:
			payload = {}
			for i in self.TANK_ADC:
				payload[i] = self.tank_levels[i]
			#logger.log_tank_levels_zap(payload)
		except Exception as e:
			logger.log('tanks_send_payload', e)

	