#!/usr/bin/env python3

# main.py
# Bix 8/28/18
# Main 

try:
	TESTING = False
	TANKS_ENABLED = False

	import emr3, logger, time, raspi, tanks

	if TANKS_ENABLED:
		import RPi.GPIO as GPIO

	if not TESTING:
		time.sleep(5)

	logger.log_start()

	CODE_VERSION = '1.0.0' 
	rubus = raspi.Raspi()
	emr = emr3.EMR3()
	DELAY_TIME = 1
	no_connection_counter = 0
	hello_sent = False
	trans_counter = 3 # default to 3 so all new trans are retrieved on startup
	loop_counter = 1

	if TANKS_ENABLED:
		tanks = tanks.Tanks()

	while True:
		if not hello_sent:
			if (rubus.mac != None):
				hello_payload = rubus.get_hello_payload()
				hello_payload['version'] = CODE_VERSION
				logger.log('main_hello_payload', hello_payload)
				hello_sent = True

		emr.get_emr_state()

		if emr.connected:
			print('Connected')

			if no_connection_counter != 0:
				logger.log('main_no_connection_counter', no_connection_counter)
				no_connection_counter = 0
			if emr.serial_num == None:
				emr.get_serial_num()
			if emr.new_trans:
				print('\nNEW TRANS\n')
				time.sleep(DELAY_TIME) 
				t = emr.get_trans()
				payload = t.make_payload()
				logger.log_transaction(payload)
				payload_zap = t.make_payload_zap()
				if not TESTING:
					logger.log_transaction_zap(payload_zap)
				trans_counter += 1
				if TANKS_ENABLED:
					tanks.update_tank_from_transaction(payload['units'])
			if trans_counter > 2: 
				emr.get_multi_trans(TESTING)
				trans_counter = 0
			if loop_counter % 600 == 0 and TANKS_ENABLED: # 600 = ~10 mins
				tanks.update_tank_levels()
			loop_counter += 1
		else:
			print('No Connection')
			no_connection_counter += 1 
		time.sleep(DELAY_TIME)

except Exception as e:
	logger.log('main', e)

finally:
	if TANKS_ENABLED:
		GPIO.cleanup()