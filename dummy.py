import pygame.camera
import pygame.image
import tellcore.telldus
import random

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
		
	def get_image(self):
		dice = int(random.random()*2)
		if dice == 0:
			return pygame.image.load("test_white.png")
		else:
			return pygame.image.load("test_black.png")
		