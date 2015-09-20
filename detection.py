import pygame
import pygame.camera
from pygame.locals import *
from dummy import Camera as dummy_Camera
import time, sys, os

class Detection:
	def __init__(self):
		self.turnoffTimestamp = 0
		self.lastSentCommand = False
		pygame.init()
		pygame.camera.init()
		if os.getenv('PYTHON_ENV', 'development') == 'production':
			camlist = pygame.camera.list_cameras()
			self.turnoffTimestamp = False
			if camlist:
				print "Camera found:", camlist[0]
				self.cam = pygame.camera.Camera(camlist[0],(640,480))
				self.cam.start()
			else:
				raise LookupError("Camera not found")
		else:
			self.cam = dummy_Camera()
	
	def lightsOn(self):
		threshold = 30
		turnoffCountdown = 120
		
		img = self.cam.get_image()
		color = pygame.transform.average_color(img)
		avg_color = (color[0]+color[1]+color[2])/3
		if avg_color > threshold and not self.lastSentCommand:
			self.lastSentCommand = True
			return True
		elif avg_color < threshold and self.lastSentCommand:
			if self.turnoffTimestamp == 0:
				self.turnoffTimestamp = int(time.time())
			if int(time.time()) - self.turnoffTimestamp > turnoffCountdown:
					self.turnoffTimestamp = 0
					self.lastSendCommand = False
					return False
			else:
				return None
		else:
			if self.turnoffTimestamp > 0:
				self.turnoffTimestamp = 0
			return None