import math

SPEED = 10 # distance moved by characters each turn
DISTANCE = 200 # distance between the center and home positions
CENTER = 600, 450 # middle of the battlefield for all characters
RIGHT_EDGE = 1300 # right side of the battlefield for fleeing enemies
LEFT_EDGE = -100 # left side of the battlefield for fleeing PCs
PUSH = 100 # distance a character gets pushed by an attack

class Entity:  

  def __init__(self, character, animation):
    self.character = character
    self.animation = animation
    self.home      = CENTER  # position at the start of each turn
    self.position  = CENTER  # current position
    self.goal      = CENTER  # current destination
    self.direction = "right" # normal facing direction
    self.state     = "healthy"
    self.target    = None

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
    if self.isAtGoal(): self.onReachingGoal()

  def onReachingGoal(self):
    if self.state == "heal":
      self.target.character.heal()
    elif self.state == "attack":
      x, y = self.target.position
      if self.facing == "right": x = x + PUSH
      else:                      x = x - PUSH
      self.target.position = x, y
      self.target.goal = self.target.home
      if self.character.attack(self.target.character):
        self.target.state == "pain"
      else:
        self.target.state == "block"
      if self.target.character.isIncapacitated():
        self.target.goal = self.target.position
    if self.character.isIncapacitated(): self.state = "incapacitated"
    elif self.character.isInjured():     self.state = "injured"
    else:                                self.state = "healthy"
    self.goal = self.home
             
  def startTurn(self):
    if self.character.isEscaping():
      self.character.escape()
    else:
      self.goal = CENTER
      
  def isTurnOver(self):
    if self.state in ("incapacitated", "injured", "healthy"):
      if self.isAtGoal(): return True
    return False

  def attack(self, target):
    self.target = target
    self.state = "attack"
    self.goal = target.home
  
  def heal(self, target):
    self.target = target
    self.state = "heal"
    self.goal = target.home
    
  def escape(self):
    self.character.tryEscaping()
    if self.facing == "right":
      self.goal = RIGHT_EDGE, self.position[1]
    else:
      self.goal = LEFT_EDGE, self.position[1]
    
  def draw(self, screen):
    if self.character.isGone() and self.isAtGoal():
      return
    frame = self.animation.getFrame(self.state, self.direction)
    screen.blit(frame, self.position)

  def getHealingTargets(self, allies):
    '''Get a list of all allies who are not healthy or escaping.'''
    targets = []
    for ally in allies:
      if not (ally.isHealthy() or ally.isEscaping()):
        targets.append(ally)
    return targets

  def getAttackTargets(self, enemies):
    '''Get a list of all enemies who are not incapacitated or gone.'''
    targets = []
    for enemy in enemies:
      if not (enemy.isGone() or enemy.isIncapacitated()):
        targets.append(enemy)
    return targets

  def randomAction(self, allies, enemies):
    '''Heal or attack a random target.'''
    if self.isHealer():
      targets = self.getHealingTargets(allies)
      if len(targets > 0):
        self.heal(random.choice(targets))
        return
    targets = self.getAttackTargets(enemies)
    if len(targets > 0):
      self.attack(random.choice(targets))

  def isEscaping(self):
    return self.character.isEscaping()

  def isGone(self):
    return self.character.isGone()

  def isInjured(self):
    return self.character.isInjured()
      
  def isIncapacitated(self):
    return self.character.isIncapacitated()

  def isHealthy(self):
    return self.character.isHealthy()

  def isHealer(self):
    return self.character.isHealer()

  def isFirst(self):
    return self.character.goesFirst()
