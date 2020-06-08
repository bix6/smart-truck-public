#!/usr/bin/env python3

# profiler.py
# Bix 10/3/18
# Tank Profiler

import emr3, time, os, RPi.GPIO as GPIO, sys, configparser

try:
	CONFIG_PATH = 'src/base/config/tanks.ini' 
	GAL_THRESHOLD = 10 # change this to modify threshold trigger

	DELAY_START = 3
	DELAY_LOOP = 1

	print('\nRunning Tank Profiler...')
	print('If you are reprofiling please clear the section')

	emr = emr3.EMR3()

	tank_num = int(input('Enter Tank Number (0-5): '))
	if tank_num<0 or tank_num>5:
		print('Invalid tank num, exiting...')
		sys.exit()
	TANK_LABEL = str(tank_num)
	topped_off = str(input('Confirm Tank Was Emptied Then Topped Off (y): ')).lower()
	if topped_off != 'y':
		print('Please top off, exiting...')
		sys.exit()
	full_tank = float(input('Enter Starting Tank Load (e.g. 120.7): '))
	if not os.path.exists(CONFIG_PATH):
		with open(CONFIG_PATH, 'w') as configfile:
			print('Creating', CONFIG_PATH)
			config = configparser.ConfigParser()
			num_tanks = int(input('Enter total number of tanks (1-6): '))
			if num_tanks<0 or num_tanks>6:
				print('Bad entry, exiting...')
				sys.exit()
			for i in range(0, num_tanks):
				config[i] = {}
			config.write(configfile)
	if not emr.start_meter():
		print('Exiting...')
		sys.exit()
	time.sleep(DELAY_START)
	TOTALIZER_START = emr.get_real_time_totalizer()
	totalizer_diff = 0
	threshold = 0
	last_res = -1
	print('Begin Pumping')

	GPIO.setmode(GPIO.BCM)

	# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
	def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	        if ((adcnum > 7) or (adcnum < 0)):
	                return -1
	        GPIO.output(cspin, True)

	        GPIO.output(clockpin, False)  # start clock low
	        GPIO.output(cspin, False)     # bring CS low

	        commandout = adcnum
	        commandout |= 0x18  # start bit + single-ended bit
	        commandout <<= 3    # we only need to send 5 bits here
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
	        
	        adcout >>= 1       # first bit is 'null' so drop it
	        return adcout

	# change these as desired - they're the pins connected from the
	# SPI port on the ADC to the Cobbler
	SPICLK = 18
	SPIMISO = 23
	SPIMOSI = 24
	SPICS = 25

	# set up the SPI interface pins
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)

	# fuel sender connected to adc #0
	potentiometer_adc = 0;

	while True:
		totalizer_cur = emr.get_real_time_totalizer()
		totalizer_diff = totalizer_cur - TOTALIZER_START
		if totalizer_diff > threshold:
			threshold += GAL_THRESHOLD
			gal_remaining = full_tank - totalizer_diff
			trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
			print('Pot:',trim_pot,'Gal:', gal_remaining)
			if trim_pot <= last_res:
				trim_pot = last_res + 1
				print('Pot adjusted: ',trim_pot,'Gal:', gal_remaining)
			with open(CONFIG_PATH, 'r+') as configfile:
				config = configparser.ConfigParser()
				config.read(CONFIG_PATH)
				config.set(TANK_LABEL, str(trim_pot), str("{0:.2f}".format(gal_remaining)))
				config.write(configfile)
				last_res = trim_pot

		time.sleep(DELAY_LOOP)

except Exception as e:
	print('Error', e)

finally:
	if GPIO.getmode() == 11:
		print('cleanup')
		GPIO.cleanup()

