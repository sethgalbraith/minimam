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
import math
import random
from animation import Animation

WHITE = 255, 255, 255
GRAY  = 64, 64, 64
BLACK = 0, 0, 0

SLOW = 20
FAST = 30

RECOIL = 100
SIDESTEP = 50

# Store animations in a dictionary with character class names as keys
# ("Warrior", "Rogue", "Wizard", "Priest", "Monster", "Dragon")
# so we don't duplicate animations for characters of the same class.
animations = {}

class Entity:  

  '''A container for characters which adds animation and movement'''

  def __init__(self, character, order, allies, NPC, ring):
    '''
    order indicates the entity's position in his party
    (0 = first, 1 = second, 2 = third, etc.)
    allies indicates the size of the entity's party.
    ring is a pygame Rect with the position and size of the combat circle.
    push is the distance a character moves back when attacked.
    speed is the distance a character moves each frame.
    '''
    classname = character.__class__.__name__
    if classname not in animations:
        animations[classname] = Animation(classname)
    self.character = character
    self.animation = animations[classname]
    self.center    = ring.center
    self.speed     = SLOW # distance moved by characters each turn
    self.backward  = False  # true for NPCs who face left by default
    self.target    = None   # enemy being attacked or ally being healed
    # find a home position for the entity and set up it's initial state.
    width = pygame.display.get_surface().get_width()
    margin = self.animation.getSize()[0] / 2 + 1
    angle = math.pi * (order + 1) / (allies + 1)
    x = math.sin(angle) * ring.width / 2
    y = math.cos(angle) * ring.height / 2
    if NPC:
      self.backward = True
      self.home = ring.centerx + x, ring.centery - y
      self.exit = width + margin,   ring.centery - y
    else:
      self.backward = False
      self.home = ring.centerx - x, ring.centery - y
      self.exit = -margin,          ring.centery - y
    self.position = self.home
    self.stand()

  # STATES

  def stand(self):
    '''Begin the standing still state'''
    self.goal = self.home
    self.nextState = self.stand
    if self.backward: self.direction = "left"
    else:             self.direction = "right"
    if self.isHealthy(): self.frame = "healthy"
    else:                self.frame = "injured"
    
  def lie(self):
    '''Begin the lying down state'''
    self.goal = self.position
    self.nextState = self.lie
    self.frame = "incapacitated"
    
  def hit(self):
    '''Begin the recoil-from-successful-attack state'''
    self.goal = self.home
    self.nextState = self.stand
    if self.backward:
        self.direction = "left"
        self.position = self.position[0] + RECOIL, self.position[1]
    else:
        self.direction = "right"
        self.position = self.position[0] - RECOIL, self.position[1]
    self.frame == "pain"

  def defend(self):
    '''Begin the avoided-attack state'''
    self.goal = self.home
    if self.isEscaping():
      self.nextState = self.fear
      if self.backward: self.direction = "right"
      else:             self.direction = "left"
    else:
      self.nextState = self.stand
      if self.backward: self.direction = "left"
      else:             self.direction = "right"
    self.position = self.position[0], self.position[1] + SIDESTEP
    self.frame == "block"

  def healSelf(self):
    '''Begin the heal-self state'''
    self.nextState = self.stand
    self.frame == "injured"
    if self.backward:
      self.direction = "left"
      self.goal = self.position[0] + RECOIL, self.position[1]
    else:
      self.direction = "right"
      self.goal = self.position[0] - RECOIL, self.position[1]
    self.character.heal()
      
  def fear(self):
    '''Begin the trying-to-escape state'''
    self.goal = self.home
    self.nextState = self.fear
    if self.backward: self.direction = "right" # notice reversed direction
    else:             self.direction = "left"  # notice reversed direction
    if self.isHealthy(): self.frame = "healthy"
    else:                self.frame = "injured"
    self.character.startEscaping()
       
  def run(self):
    '''Begin the successfully-escaped state'''
    self.goal = self.exit
    self.nextState = self.run
    if self.backward: self.direction = "right" # notice reversed direction
    else:             self.direction = "left"  # notice reversed direction
    if self.isHealthy(): self.frame = "healthy"
    else:                self.frame = "injured"
    self.character.finishEscaping()
       
  def wait(self):
    '''Begin the waiting-for-decision state'''
    self.goal = self.center
    self.nextState = self.wait
    if self.backward: self.direction = "left"
    else:             self.direction = "right"
    if self.isHealthy(): self.frame = "healthy"
    else:                self.frame = "injured"
    
  def headToAttack(self):
    '''Begin the heading-to-attack-an-enemy state'''
    self.goal = ((0.30 * self.position[0] + 0.70 * self.target.home[0]),
                 (0.30 * self.position[1] + 0.70 * self.target.home[1]))
    self.nextState = self.beginAttack
    if self.backward: self.direction = "left"
    else:             self.direction = "right"
    if self.isHealthy(): self.frame = "healthy"
    else:                self.frame = "injured"
    
  def beginAttack(self):
    '''Begin the starting-to-attack state'''
    self.goal = self.target.position
    self.nextState = self.finishAttack
    if self.backward: self.direction = "left"
    else:             self.direction = "right"
    self.frame = "attack"
    self.speed = FAST
    
  def finishAttack(self):
    '''Begin the finishing-an-attack state'''
    self.goal = ((0.30 * self.home[0] + 0.70 * self.target.home[0]),
                 (0.30 * self.home[1] + 0.70 * self.target.home[1]))
    self.nextState = self.stand
    if self.backward: self.direction = "left"
    else:             self.direction = "right"
    self.frame = "attack"
    success = self.character.attack(self.target.character)
    if self.target.isIncapacitated(): self.target.lie()
    elif success:                     self.target.hit()
    else:                             self.target.defend()
    self.speed = SLOW

  def headToHeal(self):
    '''Begin the heading-to-heal-an-ally state'''
    self.goal = ((0.30 * self.position[0] + 0.70 * self.target.home[0]),
                 (0.30 * self.position[1] + 0.70 * self.target.home[1]))
    self.nextState = self.beginHealing
    if self.backward: self.direction = "right" # notice reversed direction
    else:             self.direction = "left"  # notice reversed direction
    if self.isHealthy(): self.frame = "healthy"
    else:                self.frame = "injured"
    
  def beginHealing(self):
    '''Begin the starting-to-heal state'''
    self.goal = self.target.position
    self.nextState = self.finishHealing
    if self.backward: self.direction = "right" # notice reversed direction
    else:             self.direction = "left"  # notice reversed direction
    self.frame = "heal"
    
  def finishHealing(self):
    '''Begin the finishing-a-healing state'''
    self.goal = ((0.30 * self.home[0] + 0.70 * self.target.home[0]),
                 (0.30 * self.home[1] + 0.70 * self.target.home[1]))
    self.nextState = self.stand
    if self.backward: self.direction = "right" # notice reversed direction
    else:             self.direction = "left"  # notice reversed direction
    self.frame = "heal"
    self.target.character.heal()
    if self.target.isEscaping(): self.target.fear()
    else:                        self.target.stand()
    
  # EVENTS WHICH TRIGGER STATE CHNAGES
  
  def isAtGoal(self):
    '''Find out whether the entity has reached it's goal'''
    x = self.goal[0] - self.position[0]
    y = self.goal[1] - self.position[1]
    return math.sqrt(x * x + y * y) <= self.speed

  def move(self):
    '''Move toward goal and do next state on arrival'''
    if self.isIncapacitated(): return
    x = self.goal[0] - self.position[0]
    y = self.goal[1] - self.position[1]
    distance = math.sqrt(x * x + y * y)
    if distance > self.speed:
      x = x * self.speed / distance
      y = y * self.speed / distance
    self.position = (self.position[0] + x,
                     self.position[1] + y)
    if self.isAtGoal(): self.nextState()

  def startTurn(self):
    if self.isEscaping(): self.run()
    elif not (self.isGone() or self.isIncapacitated()): self.wait()

  def getHealingTargets(self, allies):
    '''Get a list of all allies who are not healthy or escaping.'''
    targets = []
    for ally in allies:
      if not (ally.isHealthy() or ally.isEscaping() or ally.isGone()):
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
    healing_targets = self.getHealingTargets(allies)
    attack_targets = self.getAttackTargets(enemies)
    if self.isInjured():
      if self.isHealer(): self.healSelf()
      else: self.fear()
    elif self.isHealer() and len(healing_targets) > 0:
      self.target = random.choice(healing_targets)
      self.headToHeal()
    elif len(attack_targets) > 0:
      self.target = random.choice(attack_targets)
      self.headToAttack()

  # RENDERING      

  def isMouseOver(self):
    '''Return True if the mouse is currently hovering over the entity.'''
    surface = self.animation.getFrame(self.frame, self.direction)
    rectangle = surface.get_rect()
    rectangle.midbottom = self.position
    x, y = pygame.mouse.get_pos()
    if rectangle.collidepoint(x, y):
      color = surface.get_at((x - rectangle.left, y - rectangle.top))
      if color[3] == 255: return True
    return False

  def draw(self):
    '''Draw the entity in his current state and position'''
    if self.character.isGone() and self.isAtGoal(): return
    surface = self.animation.getFrame(self.frame, self.direction)
    rectangle = surface.get_rect()
    rectangle.midbottom = self.position
    pygame.display.get_surface().blit(surface, rectangle)

  # INFORMATION
  
  def isTurnOver(self):
    if self.nextState in (self.stand, self.run, self.lie, self.fear):
      if not self.isAtGoal(): return False # try commenting this out for fun
      return True
    return False    

  def isThinking(self):
    '''True if this is the entity's turn and no action has started'''
    return self.nextState == self.wait

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
