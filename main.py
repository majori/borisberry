import tellcore.telldus
import tellcore.constants as const
import tellcore.library as lib
from detection import Detection
import time, sys, os

def main():

	# Initialize webcam and Tellstick
	try:
		dt = Detection()
		core = tellcore.telldus.TelldusCore()
		tellcore.telldus.Device(1).turn_on()
	except LookupError as e:
		print "Error when looking up for camera: ",e
		sys.exit()
	except lib.TelldusError as e:
		print "Error in Telldus: ", e
		sys.exit()
	
	# Mainloop
	while True:
		try:
			for device in core.devices():
				device.turn_on()
			lights = dt.lightsOn()
			if lights:
				for device in core.devices():
					device.turn_on()
			elif not lights:
				for device in core.devices():
					device.turn_off()
			time.sleep(1)
					
		# Catch errors
		except KeyboardInterrupt:
			print "Pressed Crtl+C!"
			dt.cam.stop()
			break
		except Exception:
			print "Something went wrong!"
			break
			
	sys.exit()

main()