#!/usr/bin/env python

import tellcore.telldus as td
import tellcore.constants as const
import tellcore.library as lib
from detection import Detection
from daemon import Daemon
import dummy

import time, sys, os, signal

def signal_term_handler(signal, frame):
    sys.exit(0)

def getTellstickDevices(tdCore):
	devices = {}
	for device in tdCore.devices():
		devices[device.name] = device
	return devices

def process():
	# Initialize webcam and Tellstick

		dt = Detection()
		if os.getenv('BORISBERRY_ENV', 'development') == 'production':
			try:
				core = td.TelldusCore()

			except LookupError as e:
				print "Error when looking up for camera: ",e
				sys.exit()
			except lib.TelldusError as e:
				print "Error in Telldus: ", e
				sys.exit()
		else:
			core = dummy.TelldusCore()
		
		devices = getTellstickDevices(core)
		signal.signal(signal.SIGTERM, signal_term_handler)
		
		# Main loop
		try:
			while True:
				lights = dt.lightsOn()
				if lights is True:
					print "Turning 'Soundsystem' on"
					devices['Soundsystem'].turn_on()
				elif lights is False:
					print "Turning 'Soundsystem' off"
					devices['Soundsystem'].turn_off()
				time.sleep(1)
		except SystemExit:
			print 'SysExit'
			sys.exit(0)
		except KeyboardInterrupt:
			sys.exit(0)

class BorisberryDaemon(Daemon):

	def run(self):
		process()

# Daemon interface
#
if __name__ == "__main__":
	pidfile = '/tmp/borisberry.pid'
	
	if len(sys.argv) == 2:
		if 'debug' == sys.argv[1]:
			process()
		else:
			os.environ['BORISBERRY_ENV'] = 'production'
			daemon = BorisberryDaemon(pidfile)
		if 'start' == sys.argv[1]:
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