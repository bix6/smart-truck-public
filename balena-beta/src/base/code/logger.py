#!/usr/bin/env python3

# logger.py
# Bix 8/28/18
# logger module

import datetime, requests, os, logging, socket, config
from logging.handlers import SysLogHandler

LOG_PATH = 'src/base/logs/log.txt'
truckID = -1

truckID = config.get_truck_id()

# papertrail logging start
class ContextFilter(logging.Filter):
	hostname = socket.gethostname()

	def filter(self, record):
		record.hostname = ContextFilter.hostname
		return True

syslog = SysLogHandler(address=('logs2.papertrailapp.com', ##papertrailID))
syslog.addFilter(ContextFilter())

format = '%(asctime)s %(hostname)s TRUCK{truckID}: %(message)s'.format(truckID=truckID)
formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')
syslog.setFormatter(formatter)

logger_pt = logging.getLogger()
logger_pt.addHandler(syslog)
logger_pt.setLevel(logging.INFO)
# papertrail logging end

def log_start():
	try:
		logger_pt.info('---LOG START---')

		if not os.path.exists(LOG_PATH):
			with open(LOG_PATH, 'w') as f:
				f.write('---LOG FILE CREATED---')

		with open(LOG_PATH, 'a') as f:
			curTime = datetime.datetime.utcnow().isoformat()
			f.write('\n\n' + curTime + '---LOG START---' + '\n')
	except Exception as e:
		print('logger_log_start', e)
		logger_pt.error('logger_log_start', e)

def log(origin, data):
	try:
		logger_pt.info(str(origin).upper() + '---' + str(data))
		print(str(origin).upper() + '---' + str(data) + '\n')
		with open(LOG_PATH, 'a') as f:
			curTime = datetime.datetime.utcnow().isoformat()
			f.write(curTime + '---' + str(origin).upper() + '---' + str(data) + '\n')
	except Exception as e:
		print('logger_log', e)
		logger_pt.error('logger_log', e)

def log_transaction(payload):
	try:
		log('log_transaction', payload)
		# url = 'http://httpbin.org/post'
		url = "filld/api/v1/trucks/{truckID}/delivery".format(truckID=truckID)
		r = requests.post(url, json=payload, headers={'Authorization':'Basic someToken'})

		if r.status_code == requests.codes.ok:
			print(r.text)
		else:
			r.raise_for_status()
	except Exception as e:
		print('logger_log_transaction', e)
		logger_pt.error('logger_log_transaction', e)

def log_transaction_zap(payload):
	try:
		log('log_transaction_zap', payload)
		url_zap = "https://hooks.zapier.com/hooks/catch/numbersAndLetter"
		r = requests.post(url_zap, json=payload)
		if r.status_code == requests.codes.ok:
			print(r.text)
		else:
			r.raise_for_status()
	except Exception as e:
		print('logger_log_transaction_zap', e)
		logger_pt.error('logger_log_transaction_zap', e)

def log_transaction_zap_dump(payload):
	try:
		log('log_transaction_zap_dump', payload)
		url_zap = "https://hooks.zapier.com/hooks/catch/numbersAndLetter"
		r = requests.post(url_zap, json=payload)
		if r.status_code == requests.codes.ok:
			print(r.text)
		else:
			r.raise_for_status()
	except Exception as e:
		print('logger_log_transaction_zap_dump', e)
		logger_pt.error('logger_log_transaction_zap_dump', e)

def log_tank_levels_zap(payload):
	try:
		payload['time'] = datetime.datetime.utcnow().isoformat()
		log('log_tank_levels_zap', payload)
		url_zap = 'https://hooks.zapier.com/hooks/catch/numbersAndLetters"
		r = requests.post(url_zap, json=payload)
		if r.status_code == requests.codes.ok:
			print(r.text)
		else:
			r.raise_for_status()
	except Exception as e:
		print('logger_log_transaction_zap_dump', e)
		logger_pt.error('logger_log_transaction_zap_dump', e)
