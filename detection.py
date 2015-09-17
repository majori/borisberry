import pygame
import pygame.camera
from pygame.locals import *

class Detection:
	def __init__(self):
		pygame.init()
		pygame.camera.init()
		camlist = pygame.camera.list_cameras()
		self.cam = ""
		if camlist:
			print "Camera found"
			self.cam = pygame.camera.Camera(camlist[0],(640,480))
		else:
			print "Camera not found, shutting down"
			exit()
	