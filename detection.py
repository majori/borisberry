import pygame
import pygame.camera
from pygame.locals import *
import sys

class Detection:
	def __init__(self):
		pygame.init()
		pygame.camera.init()
		camlist = pygame.camera.list_cameras()
		self.cam = ""
		self.lightsWereOn = False
		if camlist:
			print "Camera found:", camlist[0]
			self.cam = pygame.camera.Camera(camlist[0],(640,480))
			self.cam.start()
		else:
			raise LookupError("Camera not found")
	
	def lightsOn(self):
		img = self.cam.get_image()
		color = pygame.transform.average_color(img)
		threshold = (color[0]+color[1]+color[2])/3
		if threshold > 30 and not self.lightsWereOn:
			self.lightsWereOn = True
			return True
		elif threshold < 30 and self.lightsWereOn:
			self.lightsWereOn = False
			return False
		else:
			return None