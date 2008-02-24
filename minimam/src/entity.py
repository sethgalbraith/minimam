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

import math
import random
from animation import Animation

RIGHT = "right"  # directions are represented by strings
LEFT  = "left"   # for compatibility with the Animation class
X, Y  = 0, 1     # indices of X and Y axes in coordinate tuples

# Store animations in a dictionary with character class names as keys
# ("Warrior", "Rogue", "Wizard", "Priest", "Monster", "Dragon")
# so we don't duplicate animations for characters of the same class.
animations = {}

class Entity:  

  '''A container for characters which adds animation and movement'''

  def __init__(self, character, game):
    classname = character.__class__.__name__
    if classname not in animations:
        animations[classname] = Animation(classname)
    self.character = character
    self.animation = animations[classname]
    self.game      = game
    self.home      = game.center # position at the start of each turn
    self.exit      = game.center # a place to go when escaping
    self.position  = game.center # current position
    self.goal      = game.center # current destination
    self.direction = RIGHT       # normal facing direction
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
    x = math.sin(angle) * self.game.distance
    y = math.cos(angle) * self.game.distance * 0.75
    if NPC:
      self.direction = LEFT
      self.home = self.game.center[X] + x,          self.game.center[Y] - y
      self.exit = self.game.width + self.game.edge, self.game.center[Y] - y
    else:
      self.direction = RIGHT
      self.home = self.game.center[X] - x, self.game.center[Y] - y
      self.exit = -self.game.edge,         self.game.center[Y] - y
    self.position = self.home
    self.goal     = self.home
    
  def isAtGoal(self):
    '''Find out whether the entity has reached it's goal'''
    x = self.goal[X] - self.position[X]
    y = self.goal[Y] - self.position[Y]
    return math.sqrt(x * x + y * y) <= self.game.speed

  def move(self):
    if self.isIncapacitated():
      self.state = "incapacitated"
      return
    x = self.goal[X] - self.position[X]
    y = self.goal[Y] - self.position[Y]
    distance = math.sqrt(x * x + y * y)
    if distance > self.game.speed:
      x = x * self.game.speed / distance
      y = y * self.game.speed / distance
    self.position = (self.position[X] + x,
                     self.position[Y] + y)
    if self.isAtGoal(): self.onReachingGoal()

  def onReachingGoal(self):
    if self.isGone() or self.isEscaping(): return
    if self.state == "heal":
      self.target.character.heal()
    elif self.state == "attack":
      x, y = self.target.position
      if self.direction == RIGHT: x = x + self.game.push
      else:                       x = x - self.game.push
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
      self.goal = self.game.center
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
