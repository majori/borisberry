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
			print "Camera not found, shutting down"
			sys.exit()
	
	def lightsOn(self):
		img = self.cam.get_image()
		color = pygame.transform.average_color(img)
		if (color[0]+color[1]+color[2])/3 > 30:
			return True
		else:
			return False