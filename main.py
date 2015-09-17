import tellcore.telldus
from detection import Detection
import time

def main():
	dt = Detection()
	core = tellcore.telldus.TelldusCore()
	while True:
		if dt.lightsOn() and not dt.lightsWereOn:
			dt.lightsWereOn = True
			for device in core.devices():
				device.turn_on()
		elif not dt.lightsOn() and dt.lightsWereOn:
			dt.lightsWereOn = False
			for device in core.devices():
				device.turn_off()
		time.sleep(3)
	exit()

main()