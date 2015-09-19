import tellcore.telldus
import tellcore.constants as const
import tellcore.library as lib
import detection
import dummy

import time, sys, os



def main():

	# Initialize webcam and Tellstick
	dt = detection.Detection()
	if os.getenv('PYTHON_ENV', 'development') == 'production':
		try:
			core = tellcore.telldus.TelldusCore()
			device = tellcore.telldus.Devices
			tellcore.telldus.Device(1).turn_on()
		except LookupError as e:
			print "Error when looking up for camera: ",e
			sys.exit()
		except lib.TelldusError as e:
			print "Error in Telldus: ", e
			sys.exit()
	else:
		core = dummy.TelldusCore()
		device = dummy.Devices
	
	# Mainloop
	while True:
		try:
			lights = dt.lightsOn()
			if lights is True:
				for device in core.devices():
					device.turn_on()
			elif lights is False:
				for device in core.devices():
					device.turn_off()
			time.sleep(1)
					
		# Catch errors
		except KeyboardInterrupt:
			print "Pressed Crtl+C!"
			dt.cam.stop()
			break
			
	sys.exit()

main()