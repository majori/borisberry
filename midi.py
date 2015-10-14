#!/usr/bin/env python
import time
import logging
import rtmidi

logger = logging.getLogger('borisberry')

MIDI_DEVICE='ProdipeMIDIlilo'

class Midi:

	def __init__(self):
		self.midiout = rtmidi.MidiOut()
		available_ports = self.midiout.get_ports()

		if available_ports:
			x = 0
			for port in available_ports:
				if MIDI_DEVICE in port:
					self.midiout.open_port(x)
				x += 1
		else:
			self.midiout.open_virtual_port("My virtual output")

	def __del__(self):
		del self.midiout

	def send_message(self, msg):
		if len(msg) != 3:
			logger.error('MIDI message didnt have 3 components!')
			return
		logger.debug('Sending MIDI message: ' + str(msg[0]) + ', ' + str(msg[1]) + ', ' + str(msg[2]))
		self.midiout.send_message(msg)
		return

	def flicker(self, interval):
		note_on = [0x90, 60, 60] # note on, channel 1, middle C, velocity 60
		note_off = [0x80, 60, 0] # note off, channel 1, middle C, velocity 0
		self.send_message(note_on)
		time.sleep(interval)
		self.send_message(note_off)
		time.sleep(interval)
		return

		