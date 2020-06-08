#!/usr/bin/env python3

# raspi.py
# Bix 8/28/18
# raspi Module

import logger, os, socket, config

class Raspi:
	"""Raspi Class"""

	def get_mac(self, interface='wlan0'):
		try:
			with open('/sys/class/net/%s/address' %interface, 'r') as f:
				self.mac = f.read()[0:17]
		except Exception as e:
			logger.log('raspi_get_mac', e)

	def get_serial(self):
		try:
			with open('/proc/cpuinfo','r') as f:
				for line in f:
					if line[0:6]=='Serial':
						self.serial = line[10:26]
		except Exception as e:
			logger.log('raspi_get_serial', e)

	def get_hostname(self):
		try:
			self.hostname = socket.gethostname()
		except Exception as e:
			logger.log('raspi_get_hostname', e)

	def get_truck_id(self):
		try:
			self.truck_id = config.get_truck_id()
		except Exception as e:
			logger.log('raspi_get_truck_id', e)

	def get_temp(self):
		try:
			temp = os.popen("vcgencmd measure_temp").readline()
			temp = temp.replace("temp=","")
			self.temp = float(temp.replace("'C\n", ""))
		except Exception as e:
			logger.log('raspi_get_temp', e)

	def __init__(self):
		self.mac = None
		self.serial = None
		self.hostname = None
		self.truck_id = -1
		self.temp = -1

		if os.uname()[4].startswith("arm"):
			self.get_mac('wlan0')
			self.get_serial()
			self.get_hostname()
			self.get_truck_id()
			self.get_temp()

	def get_hello_payload(self):
		payload = {}
		payload['mac'] = self.mac
		payload['serial'] = self.serial
		payload['hostname'] = self.hostname
		payload['truck_id'] = self.truck_id
		payload['temp'] = self.temp
		return payload