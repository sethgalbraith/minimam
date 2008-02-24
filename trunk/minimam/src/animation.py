# Copyright 2008 Seth Galbraith
#
# This file is part of Minimam.
#
# Minimam is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Minimam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Minimam.  If not, see <http://www.gnu.org/licenses/>.

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
		classname = classname.lower()
		for direction in DIRECTIONS:
			for state in STATES:
				try:
					filename = "%s-%s-%s.png" % (classname, state, direction)
					surface = pygame.image.load(filename)
					self.frames[direction][state] = surface 
				except pygame.error:
					try:
						filename = "%s-%s.png" % (classname, state)
						surface = pygame.image.load(filename)
						if direction == "left":
							surface = pygame.transform.flip(surface, True, False)
						self.frames[direction][state] = surface
					except pygame.error:
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