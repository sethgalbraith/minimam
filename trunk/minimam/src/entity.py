import math

SPEED    = 10   # distance moved by characters each turn
DISTANCE = 200  # distance between the center and home positions
center   = 0, 0 # middle of the battlefield for all characters

class Entity:	
	
	def __init__(self, character = None):
		self.character = None
		self.home      = 0, 0    # position at the start of each turn
		self.position  = 0, 0    # current position
		self.goal      = 0, 0    # current destination
		self.direction = "right" # normal facing direction

	def setHome(self, order, allies):
		'''
		Find a home position for the character.
		order indicates the character's position in his party
		(0 = first, 1 = second, 2 = third, etc.)
		allies indicates the size of the character's party.
		'''
		angle = math.pi * (order + 1) / (allies + 1)
		x = math.cos(angle) * DISTANCE
		y = math.sin(angle) * DISTANCE
		if self.direction == "right": x = -x
		self.home = x, y
		
	def isAtGoal(self):
		'''Find out whether the character has reached it's goal'''
		x = self.goal[0] - self.position[0]
		y = self.goal[1] - self.position[1]
		return math.sqrt(x * x, y * y) <= SPEED

	def move(self):
		x = self.goal[0] - self.position[0]
		y = self.goal[1] - self.position[1]
		distance = math.sqrt(x * x, y * y)
		if distance > SPEED:
			x = x * SPEED / distance
			y = y * SPEED / distance
		self.position = self.position[x] + x, self.position[y] + y
		