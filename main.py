#!/usr/bin/env python

import tellcore.telldus as td
import tellcore.constants as const
import tellcore.library as lib
from detection import Detection
from daemon import Daemon
import dummy

import time, sys, atexit, os, signal, logging
from logging.handlers import RotatingFileHandler

# Setup logger
class NullHandler(logging.Handler):
	def emit(self,record):
		pass

logger = logging.getLogger('borisberry')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
h = NullHandler()
logger.addHandler(h)

# Catch SYSTERM
def signal_term_handler(signal, frame):
	sys.exit(0)

def getTellstickDevices(tdCore):
	devices = {}
	for device in tdCore.devices():
		devices[device.name] = device
	return devices

def process():
	# Initialize webcam and Tellstick
		logger.info('------Process started!-------')
		dt = Detection()
		if os.getenv('BORISBERRY_ENV', 'development') == 'production':
			try:
				core = td.TelldusCore()

			except LookupError as e:
				logger.error('Error when looking up for camera: ' + e)
				sys.exit()
			except lib.TelldusError as e:
				logger.error('Error in Telldus: ' + e)
				sys.exit()
		else:
			core = dummy.TelldusCore()

		devices = getTellstickDevices(core)

		# Main loop
		try:
			while True:
				lights = dt.lightsOn()
				if lights is True:
					logger.info('Turning "Soundsystem" on')
					devices['Soundsystem'].turn_on()
				elif lights is False:
					logger.info('Turning "Soundsystem" off')
					devices['Soundsystem'].turn_off()
				time.sleep(1)
		except KeyboardInterrupt:
			sys.exit(0)

# If daemon is used, define run()
class BorisberryDaemon(Daemon):

	def run(self):
		process()

# Daemon interface
#
signal.signal(signal.SIGTERM, signal_term_handler)

if __name__ == "__main__":

	if len(sys.argv) == 2:
		if 'debug' == sys.argv[1]:
			# Setup logging to console
			ch = logging.StreamHandler()
			ch.setFormatter(formatter)
			logger.addHandler(ch)
			logger.setLevel(logging.DEBUG)

			process()
		else:
			daemon = BorisberryDaemon('/tmp/borisberry.pid')

		if 'start' == sys.argv[1]:
			# Setup logging to file
			hdlr = RotatingFileHandler('/var/tmp/borisberry.log', maxBytes=5*1024*1024, backupCount=2)
			hdlr.setFormatter(formatter)
			logger.addHandler(hdlr)
			logger.setLevel(logging.INFO)

			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|debug" % sys.argv[0]
		sys.exit(2)