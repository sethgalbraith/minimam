import math
import random
from animation import Animation

SPEED = 10        # distance moved by characters each turn
DISTANCE = 200    # distance between the center and home positions
CENTER = 600, 450 # middle of the battlefield for all characters
RIGHT_EDGE = 1300 # right side of the battlefield for fleeing enemies
LEFT_EDGE = -100  # left side of the battlefield for fleeing PCs
PUSH = 100        # distance a character gets pushed by an attack

RIGHT = "right"  # directions are represented by strings
LEFT  = "left"   # for compatibility with the Animation class

X, Y = 0, 1

# Store animations in a dictionary with character class names as keys
# ("Warrior", "Rogue", "Wizard", "Priest", "Monster", "Dragon")
# so we don't duplicate animations for characters of the same class.
animations = {}

class Entity:  

  '''A container for characters which adds animation and movement'''

  def __init__(self, character):
    classname = character.__class__.__name__
    if classname not in animations:
        animations[classname] = Animation(classname)
    self.character = character
    self.animation = animations[classname]
    self.home      = CENTER  # position at the start of each turn
    self.exit      = CENTER  # a place to go when escaping
    self.position  = CENTER  # current position
    self.goal      = CENTER  # current destination
    self.direction = RIGHT   # normal facing direction
    self.state     = "healthy"
    self.target    = None
    self.thinking  = False

  def setHome(self, order, allies, NPC):
    '''
    Find a home position for the entity.
    order indicates the entity's position in his party
    (0 = first, 1 = second, 2 = third, etc.)
    allies indicates the size of the entity's party.
    '''
    angle = math.pi * (order + 1) / (allies + 1)
    x = math.sin(angle) * DISTANCE
    y = math.cos(angle) * DISTANCE
    if NPC:
      self.direction = LEFT
      self.home = CENTER[X] + x, CENTER[Y] - y
      self.exit = RIGHT_EDGE,    CENTER[Y] - y
    else:
      self.direction = RIGHT
      self.home = CENTER[X] - x, CENTER[Y] - y
      self.exit = LEFT_EDGE,     CENTER[Y] - y
    self.position = self.home
    self.goal     = self.home
    
  def isAtGoal(self):
    '''Find out whether the entity has reached it's goal'''
    x = self.goal[X] - self.position[X]
    y = self.goal[Y] - self.position[Y]
    return math.sqrt(x * x + y * y) <= SPEED

  def move(self):
    if self.isIncapacitated():
      self.state = "incapacitated"
      return
    x = self.goal[X] - self.position[X]
    y = self.goal[Y] - self.position[Y]
    distance = math.sqrt(x * x + y * y)
    if distance > SPEED:
      x = x * SPEED / distance
      y = y * SPEED / distance
    self.position = (self.position[X] + x,
                     self.position[Y] + y)
    if self.isAtGoal(): self.onReachingGoal()

  def onReachingGoal(self):
    if self.isGone() or self.isEscaping(): return
    if self.state == "heal":
      self.target.character.heal()
    elif self.state == "attack":
      x, y = self.target.position
      if self.direction == RIGHT: x = x + PUSH
      else:                       x = x - PUSH
      self.target.position = x, y
      self.target.goal = self.target.home
      hit = self.character.attack(self.target.character)
      if hit: self.target.state == "pain"
      else:   self.target.state == "block"
    if self.isIncapacitated(): self.state = "incapacitated"
    elif self.isInjured():     self.state = "injured"
    else:                      self.state = "healthy"
    self.goal = self.home
             
  def startTurn(self):
    if self.isEscaping():
      self.character.finishEscaping()
      self.goal = self.exit
      self.thinking = False
    elif not self.isGone():
      self.goal = CENTER
      self.thinking = True
      
  def isTurnOver(self):
    if self.state in ("incapacitated", "injured", "healthy"):
      if self.isAtGoal() and not self.thinking: return True
    return False

  def attack(self, target):
    '''Attack an enemy'''
    self.target = target
    self.state = "attack"
    self.goal = target.home
    self.thinking = False
  
  def heal(self, target):
    '''Heal an ally'''
    self.target = target
    self.state = "heal"
    self.goal = target.home
    self.thinking = False
    
  def escape(self):
    '''Try to escape'''
    self.character.startEscaping()
    self.goal = self.home
    self.thinking = False
    
  def draw(self, screen):
    '''Draw the entity in his current state and position'''
    if self.character.isGone() and self.isAtGoal(): return
    if self.state == "heal" or self.isEscaping() or self.isGone():
      if self.direction == RIGHT: direction = LEFT
      else:                       direction = RIGHT
    else:                         direction = self.direction
    frame = self.animation.getFrame(self.state, direction)
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
    '''Escape, heal or attack a random target.'''
    if self.isInjured():
      self.escape()
      return
    if self.isHealer():
      targets = self.getHealingTargets(allies)
      if len(targets) > 0:
        self.heal(random.choice(targets))
        return
    targets = self.getAttackTargets(enemies)
    if len(targets) > 0:
      self.attack(random.choice(targets))

  def isThinking(self):
    '''True if this is the entity's turn and no action has started'''
    return self.thinking

  def isEscaping(self):
    '''True if the entity is trying to escape but can still be stopped'''
    return self.character.isEscaping()

  def isGone(self):
    '''
    True if the entity has successfully escaped.
    The entity may still be visible, leaving the battlefield.
    '''
    return self.character.isGone()

  def isInjured(self):
    '''True if the entity is injured but not incapacitated'''
    return self.character.isInjured()
      
  def isIncapacitated(self):
    '''True if the entity is incapacitated (not standing)'''
    return self.character.isIncapacitated()

  def isHealthy(self):
    '''True if the entity is healthy (not injured or incapacitated)'''
    return self.character.isHealthy()

  def isHealer(self):
    '''True if the entity has the ability to heal allies'''
    return self.character.isHealer()

  def isFirst(self):
    '''
    True if the entity is a Rogue or Dragon
    whose turns happen before other classes
    '''
    return self.character.isFirst()
