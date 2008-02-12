import pygame

DIRECTIONS = "left", "right"
STATES = "healthy", "injured", "incapacitated", "attack", "pain", "defend", "heal"

class Animation:
	
	def __init__(self, classname = None):
		self.frames = {}
		for direction in DIRECTIONS:
			self.frames[direction] = {}
			for state in STATES:
				self.frames[direction][state] = None		
		if classname is not None: self.loadFrames(classname)
		
	def loadFrames(self, classname):
		for direction in DIRECTIONS:
			for state in STATES:
				try:
					filename = "%s_%s_%s.png" % (classname, state, direction)
					surface = pygame.image.load(filename)
					self.frames[direction][state] = surface 
				except IOError:
					try:
						filename = "%s_%s.png" % (classname, state)
						surface = pygame.image.load(filename)
						if direction == "left":
							surface = pygame.transform.mirror(surface)
						self.frames[direction][state] = surface
					except IOError:
						pass

	def getFrame(self, state, direction):
		frame = self.frames[direction][state]
		if frame is None:
			if state == "heal":
				frame = self.frames[direction]["attack"]
			if state == "block":
				frame = self.frames[direction]["healthy"]
			if state == "pain":
				frame = self.frames[direction]["injured"]
		return frame