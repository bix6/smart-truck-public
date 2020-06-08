#!/usr/bin/env python3

# config.py
# Bix 10/4/18
# config module

import configparser, logger

CONFIG_PATH = 'src/base/config/init.ini'
CONFIG_PATH_TANKS = 'src/base/config/tanks.ini'

def get_truck_id():
	try:
		config = configparser.ConfigParser()
		config.read(CONFIG_PATH)
		return config['Truck']['truck_id']
	except Exception as e:
		logger.log('config_get_truck_id', e)

def get_unit_type():
	try:
		config = configparser.ConfigParser()
		config.read(CONFIG_PATH)
		return config['EMR']['unit_type']
	except Exception as e:
		logger.log('config_get_unit_type', e)

def get_last_sale_sent():
	try:
		config = configparser.ConfigParser()
		config.read(CONFIG_PATH)
		return int(config['EMR']['last_sale_sent'])
	except Exception as e:
		logger.log('config_get_last_sale_sent', e)

def set_last_sale_sent(lss_in):
	try:
		with open(CONFIG_PATH, 'r+') as configfile:
			config = configparser.ConfigParser()
			config.read(CONFIG_PATH)
			config.set('EMR','last_sale_sent', lss_in)
			config.write(configfile)
	except Exception as e:
		logger.log('config_set_last_sale_sent', e)

def get_tank_level(tank_in):
	try:
		config = configparser.ConfigParser()
		config.read(CONFIG_PATH)
		return float(config['Tanks'][str(tank_in)])
	except Exception as e:
		logger.log('config_get_tank_level', e)

def get_lookup_table(tank_in):
	try:
		config = configparser.ConfigParser()
		config.read(CONFIG_PATH_TANKS)
		return dict(config.items(str(tank_in)))
	except Exception as e:
		logger.log('config_get_lookup_table', e)

def update_tank_level(tank_in, amt_in):
	try:
		with open(CONFIG_PATH, 'r+') as configfile:
			config = configparser.ConfigParser()
			config.read(CONFIG_PATH)
			config.set('Tanks', str(tank_in), str(amt_in))
			config.write(configfile)
	except Exception as e:
		logger.log('config_update_tank_level', e)

def get_num_tanks():
	try:
		config = configparser.ConfigParser()
		config.read(CONFIG_PATH_TANKS)
		return len(config.sections())
	except Exception as e:
		logger.log('config_get_num_tanks', e)

def get_timezone():
	try:
		config = configparser.ConfigParser()
		config.read(CONFIG_PATH)
		return config['Truck']['timezone']
	except Exception as e:
		logger.log('config_get_tank_level', e)

