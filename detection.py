import pygame
import pygame.camera
from pygame.locals import *

class Detection:
	def __init__(self):
		pygame.init()
		pygame.camera.init()
		camlist = pygame.camera.list_cameras()
		self.cam = ""
		self.lightsWereOn = False
		if camlist:
			print "Camera found"
			self.cam = pygame.camera.Camera(camlist[0],(640,480))
		else:
			print "Camera not found, shutting down"
			exit()
	
	def lightsOn(self):
		self.cam.start()
		img = self.cam.get_image()
		self.cam.stop()
		color = pygame.transform.average_color(img)
		if (color[0]+color[1]+color[2])/3 > 30:
			return True
		else:
			return False