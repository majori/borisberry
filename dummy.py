# This module allows program run even if there is no webcam
# or Tellstick attached to computer.

import pygame.camera
import pygame.image
import tellcore.telldus
import time

class TelldusCore(tellcore.telldus.TelldusCore):
	def devices(self):
		return [Devices(1)]

class Devices(tellcore.telldus.Device):
	def command_sent(self, command):
		print 'DummyModule: sent', command, '-command to', self.name
	
	def bell(self):
		self.command_sent('bell')
	
	def dim(self):
		self.command_sent('dim')
		
	def up(self):
		self.command_sent('up')
	
	def down(self):
		self.command_sent('down')
		
	def execute(self):
		self.command_sent('execute')
		
	def learn(self):
		self.command_sent('learn')
		
	def stop(self):
		self.command_sent('stop')
		
	def turn_off(self):
		self.command_sent('turn_off')
		
	def turn_on(self):
		self.command_sent('turn_on')
	

class Camera(pygame.camera.Camera):
	def __init__(self):
		self.type = 'dummy'
	
	# This function replaces pygame's image capture function.
	# Instead of taking a image, switch between dark and
	# white image every 10 second
	def get_image(self):
		interval = 20
		sec = int(time.strftime('%S')) % interval
		if sec < interval/2:
			return pygame.image.load("test_white.png")
		else:
			return pygame.image.load("test_black.png")
		