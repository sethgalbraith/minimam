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
    self.speed = 10 # distance moved by characters each turn
    self.push = 100 # distance a character gets pushed by an attack
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

  def isMouseOver(self):
    width, height = self.animation.getSize()
    area = pygame.Rect(0, 0, width, height)
    area.centerx = self.position[0]
    area.bottom = self.position[1]
    x, y = pygame.mouse.get_pos()
    return area.collidepoint(x, y)


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
    
  def recoil(self, hit = False):
    '''Begin the recoil-from-attack state'''
    self.goal = self.home
    self.nextThink = self.stand
    x, y = self.position
    if self.backward:
        if self.isEscaping(): self.direction = "right"
        else:                 self.direction = "left"
        x = x + self.push
    else:
        if self.isEscaping(): self.direction = "left"
        else:                 self.direction = "right"
        x = x - self.push
    self.position = x, y
    if hit: self.frame == "pain"
    else:   self.frame == "block"
      
  def healSelf(self):
    '''Begin the heal-self state'''
    self.nextState = self.stand
    self.frame == "injured"
    if self.backward:
      self.direction = "left"
      self.goal = self.position[0] + self.push, self.position[1]
    else:
      self.direction = "right"
      self.goal = self.position[0] - self.push, self.position[1]
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
    self.goal = ((0.20 * self.position[0] + 0.80 * self.target.home[0]),
                 (0.20 * self.position[1] + 0.80 * self.target.home[1]))
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
    
  def finishAttack(self):
    '''Begin the finishing-an-attack state'''
    self.goal = ((0.30 * self.home[0] + 0.70 * self.target.home[0]),
                 (0.30 * self.home[1] + 0.70 * self.target.home[1]))
    self.nextState = self.stand
    if self.backward: self.direction = "left"
    else:             self.direction = "right"
    self.frame = "attack"
    hit = self.character.attack(self.target.character)
    if self.target.isIncapacitated(): self.target.lie()
    else: self.target.recoil(hit)

  def headToHeal(self):
    '''Begin the heading-to-heal-an-ally state'''
    self.goal = ((0.25 * self.position[0] + 0.75 * self.target.home[0]),
                 (0.25 * self.position[1] + 0.75 * self.target.home[1]))
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
    self.goal = ((0.25 * self.home[0] + 0.75 * self.target.home[0]),
                 (0.25 * self.home[1] + 0.75 * self.target.home[1]))
    self.nextState = self.stand
    if self.backward: self.direction = "right" # notice reversed direction
    else:             self.direction = "left"  # notice reversed direction
    self.frame = "heal"
    self.target.character.heal()
    self.target.stand()
    
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

  def draw(self, screen):
    '''Draw the entity in his current state and position'''
    #if self.character.isGone() and self.isAtGoal(): return
    surf = self.animation.getFrame(self.frame, self.direction)
    x, y = self.position
    width, height = surf.get_rect().size
    screen.blit(surf, (x - width / 2, y - height))

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
