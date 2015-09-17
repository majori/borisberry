import tellcore.telldus
from detection import Detection
import time, sys


def main():
	dt = Detection()
	core = tellcore.telldus.TelldusCore()
	while True:
		try:
			if dt.lightsOn() and not dt.lightsWereOn:
				dt.lightsWereOn = True
				for device in core.devices():
					device.turn_on()
			elif not dt.lightsOn() and dt.lightsWereOn:
				dt.lightsWereOn = False
				for device in core.devices():
					device.turn_off()
			time.sleep(3)
		except KeyboardInterrupt:
			print "Pressed Crtl+C!"
			dt.cam.stop()
			sys.exit()

main()