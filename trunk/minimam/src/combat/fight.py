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

from entity import Entity
from background import Background
from button import Button

import pygame

def splitByClass(entities):
  '''Separate Rogues and Dragons from other characters.'''
  slow, fast = [], []
  for entity in entities:
    if entity.isFirst(): fast.append(entity)
    else:                slow.append(entity)
  return fast, slow

def alternateTurns(first, second):
  '''
  Combine two lists, alternating items from 1st and 2nd list
  until there are no more items in the one of the lists,
  with the remaining items from the longer list at the end.
  '''
  turns = []
  for i in range(max(len(first), len(second))):
    if (i < len(first)):  turns.append(first[i])
    if (i < len(second)): turns.append(second[i])
  return turns

def isDefeated(entities):
  '''True if these entities are all incapacitated or gone'''
  for entity in entities:
    if not (entity.isIncapacitated() or entity.isGone()):
      return False
  return True

class Fight:
  
  def __init__(self, PCs = [], NPCs = []):
    self.delay = 10 # duration of animation frames in milliseconds
    screen = pygame.display.get_surface()
    self.ring = pygame.rect.Rect(0, 0, 600, 300) # combat circle
    self.ring.centerx = screen.get_width() / 2
    self.ring.bottom = screen.get_height()
    self.background = Background('graphics/All_Gizah_Pyramids-cropped.jpg')
    self.setPlayerCharacters(PCs)
    self.setNonPlayerCharacters(NPCs)
    self.quit = False
    self.escape = Button('escape')
    rect = self.escape.rect
    rect.bottom = screen.get_height() - 20
    rect.left = 20
    self.heal = pygame.image.load("graphics/heal.png").convert_alpha()
    self.attack = pygame.image.load("graphics/attack.png").convert_alpha()
    
  def setPlayerCharacters(self, PCs):
    self.PCs = []
    for i in range(len(PCs)):
      self.PCs.append(Entity(PCs[i], i, len(PCs), False, self.ring))
  
  def setNonPlayerCharacters(self, NPCs):
    self.NPCs = []
    for i in range(len(NPCs)):
      self.NPCs.append(Entity(NPCs[i], i, len(NPCs), True, self.ring))
    
  def sortedEntities(self):
    '''
    Combine the PC and NPC lists
    in the order of the character's turns.
    '''
    fastPCs,  slowPCs  = splitByClass(self.PCs)
    fastNPCs, slowNPCs = splitByClass(self.NPCs)
    fast = alternateTurns(fastPCs, fastNPCs)
    slow = alternateTurns(slowPCs, slowNPCs)
    return fast + slow
 
  def toggleFullscreen(self):
    screen = pygame.display.get_surface()
    if screen.get_flags() & pygame.FULLSCREEN:
      pygame.display.set_mode(screen.get_size())
    else:
      pygame.display.set_mode(screen.get_size(), pygame.FULLSCREEN)
 
  def selectLeft(self):
    '''Select the previous party or option.'''
    if not self.entity.isThinking(): return
    elif self.entity in self.NPCs: return
    elif self.entity.target == None:        self.entity.target = self.NPCs[0]
    elif self.entity.target == self.escape: self.entity.target = None
    elif self.entity.target in self.PCs:    self.entity.target = self.escape
    elif self.entity.target in self.NPCs:   self.entity.target = self.PCs[0]
 
  def selectRight(self):
    '''Select the next party or option.'''
    if not self.entity.isThinking(): return
    elif self.entity in self.NPCs: return
    elif self.entity.target == None:        self.entity.target = self.escape
    elif self.entity.target == self.escape: self.entity.target = self.PCs[0]
    elif self.entity.target in self.PCs:    self.entity.target = self.NPCs[0]
    elif self.entity.target in self.NPCs:   self.entity.target = None
      
  def selectUp(self):
    '''Select the previous character in the party or the previous party.'''
    if not self.entity.isThinking(): return
    elif self.entity in self.NPCs: return
    elif self.entity.target == None:        self.entity.target = self.NPCs[-1]
    elif self.entity.target == self.escape: self.entity.target = None
    elif self.entity.target in self.PCs:
      index = self.PCs.index(self.entity.target)
      if index == 0: self.entity.target = self.escape
      else:          self.entity.target = self.PCs[index - 1]        
    elif self.entity.target in self.NPCs:
      index = self.NPCs.index(self.entity.target)
      if index == 0: self.entity.target = self.PCs[-1]
      else:          self.entity.target = self.NPCs[index - 1]
 
  def selectDown(self):
    '''Select the next character in the party or the next party.'''
    if not self.entity.isThinking(): return
    elif self.entity in self.NPCs: return
    elif self.entity.target == None:        self.entity.target = self.escape
    elif self.entity.target == self.escape: self.entity.target = self.PCs[0]
    elif self.entity.target in self.PCs:
      index = self.PCs.index(self.entity.target)
      if index == len(self.PCs) - 1: self.entity.target = self.NPCs[0]
      else:                          self.entity.target = self.PCs[index + 1]        
    elif self.entity.target in self.NPCs:
      index = self.NPCs.index(self.entity.target)
      if index == len(self.NPCs) - 1: self.entity.target = None
      else:                           self.entity.target = self.NPCs[index + 1]
 
  def selectMouse(self):
    '''Select the nearest character under the mouse pointer.'''
    if not self.entity.isThinking(): return
    elif self.entity in self.NPCs: return
    #entity.target = None
    buttons = [self.escape] + self.NPCs + self.PCs
    buttons.reverse()
    for button in buttons:
      if button.isMouseOver():
        self.entity.target = button
        break
 
  def chooseAction(self):
    '''Escape, heal or attack the selected target.'''
    if not self.entity.isThinking(): return
    elif self.entity in self.NPCs: return
    elif self.entity.target == self.escape: self.entity.fear()
    elif self.entity.target in self.PCs and self.entity.isHealer():
      if self.entity.target.isInjured() or self.entity.target.isIncapacitated():
        if self.entity.target == self.entity: self.entity.healSelf()
        else:                                 self.entity.headToHeal()
    elif self.entity.target in self.NPCs:
      if not self.entity.target.isGone():
        if not self.entity.target.isIncapacitated():
          self.entity.headToAttack()

 
  def input(self):
    '''Respond to user interface events'''
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit = True
      elif event.type == pygame.KEYDOWN:
        if   event.key == pygame.K_ESCAPE: self.quit = True
        elif event.key == pygame.K_F11:    self.toggleFullscreen()
        elif event.key == pygame.K_LEFT:   self.selectLeft()
        elif event.key == pygame.K_RIGHT:  self.selectRight()
        elif event.key == pygame.K_UP:     self.selectUp()
        elif event.key == pygame.K_DOWN:   self.selectDown()
        elif event.key == pygame.K_RETURN: self.chooseAction()
      elif event.type == pygame.MOUSEMOTION: self.selectMouse()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        self.selectMouse()
        self.chooseAction()
    pygame.event.pump()

  def think(self):
    '''Entities move and make decisions'''
    if self.entity.isThinking() and self.entity in self.NPCs:
      self.entity.randomAction(self.NPCs, self.PCs)
    for entity in self.PCs:  entity.move()
    for entity in self.NPCs: entity.move()

  def drawSelector(self):
    '''Draw a selector under the target if it is a PC or NPC'''
    if self.entity.target == None: return
    if self.entity.target == self.escape: return
    entity_team = self.entity in self.PCs
    target_team = self.entity.target in self.PCs
    if not (entity_team or target_team): selector = self.heal
    elif entity_team and target_team:    selector = self.heal
    else:                                selector = self.attack
    rectangle = selector.get_rect()
    rectangle.midbottom = self.entity.target.position
    rectangle.bottom = rectangle.bottom + 15
    pygame.display.get_surface().blit(selector, rectangle)

  def drawEntities(self):
    '''Draw the entities representing each character'''
    entities = self.PCs + self.NPCs
    entities.sort(lambda a, b: int(a.position[1] - b.position[1]))
    for entity in entities: entity.draw()

  def draw(self):
    '''Draw the fight scene'''
    self.background.draw()
    self.drawSelector()
    self.drawEntities()
    self.escape.draw(self.entity.target == self.escape)
    pygame.display.flip()

  def turn(self):
    '''One character's turn'''
    if self.entity.isIncapacitated() or self.entity.isGone(): return
    self.entity.startTurn()
    while not (self.quit or self.entity.isTurnOver()):
      self.input()
      self.think()
      self.draw()
      pygame.time.wait(self.delay)

  def loop(self):
    '''Take turns until the PCs or NPCs are defeated'''
    entities = self.sortedEntities()
    turn = 0
    while not self.quit:
      if isDefeated(self.PCs):  return
      if isDefeated(self.NPCs): return
      self.entity = entities[turn]
      self.turn()
      turn = turn + 1
      if turn == len(entities): turn = 0

# self test

if __name__ == "__main__":
  
  from character.warrior import Warrior
  from character.rogue   import Rogue
  from character.wizard  import Wizard
  from character.priest  import Priest
  from character.monster import Monster
  from character.dragon  import Dragon
  
  import random

  RESOLUTIONS = [
    (1680, 1050), # WSXGA+
    (1600, 1200), # UXGA
    (1440, 900),  # ulrich's laptop
    (1400, 1050), # SXGA+
    (1280, 1024), # WXGA
    (1280, 800),  # my laptop
    (1200, 900),  # OLPC XO-1
    (1024, 768),  # XGA
    (800, 600),   # SVGA
    (800, 480),   # WVGA (Eee PC, CloudBook)
    (640, 480)]   # VGA
  
  pygame.init()
  for resolution in RESOLUTIONS:
    if pygame.display.mode_ok(resolution, pygame.FULLSCREEN):
      pygame.display.set_mode(resolution, pygame.FULLSCREEN)
      break
  pygame.mouse.set_visible(True)

  import os; os.chdir('..') # so you can find the graphics
  
  fight = Fight()
  while not fight.quit:
    choice = random.randrange(3)
    if choice == 0:
      PCs = [Warrior(), Warrior(), Warrior()]
      NPCs = [Rogue(), Rogue(), Rogue(), Rogue()]
    if choice == 1:
      PCs = [Rogue(), Warrior(), Rogue(), Warrior(), Rogue()]
      NPCs = [Dragon(), Dragon()]
    if choice == 2:
      PCs = [Priest(), Rogue(), Warrior(), Wizard()]
      for character in PCs: character.setLevel(1)
      NPCs = [Monster(), Monster(), Dragon(), Monster(), Monster()]
      NPCs[2].setLevel(2)
    fight.setPlayerCharacters(PCs)
    fight.setNonPlayerCharacters(NPCs)
    fight.loop()
