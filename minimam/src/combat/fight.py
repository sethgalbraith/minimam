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
    self.selected = None
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
    if self.selected == None:          self.selected = self.NPCs[0]
    elif self.selected == self.escape: self.selected = None
    elif self.selected in self.PCs:    self.selected = self.escape
    elif self.selected in self.NPCs:   self.selected = self.PCs[0]
 
  def selectRight(self):
    '''Select the next party or option.'''
    if self.selected == None:          self.selected = self.escape
    elif self.selected == self.escape: self.selected = self.PCs[0]
    elif self.selected in self.PCs:    self.selected = self.NPCs[0]
    elif self.selected in self.NPCs:   self.selected = None
      
  def selectUp(self):
    '''Select the previous character in the party or the previous party.'''
    if self.selected == None:          self.selected = self.NPCs[-1]
    elif self.selected == self.escape: self.selected = None
    elif self.selected in self.PCs:
      index = self.PCs.index(self.selected)
      if index == 0: self.selected = self.escape
      else:          self.selected = self.PCs[index - 1]        
    elif self.selected in self.NPCs:
      index = self.NPCs.index(self.selected)
      if index == 0: self.selected = self.PCs[-1]
      else:          self.selected = self.NPCs[index - 1]
 
  def selectDown(self):
    '''Select the next character in the party or the next party.'''
    if self.selected == None:          self.selected = self.escape
    elif self.selected == self.escape: self.selected = self.PCs[0]
    elif self.selected in self.PCs:
      index = self.PCs.index(self.selected)
      if index == len(self.PCs) - 1: self.selected = self.NPCs[0]
      else:                          self.selected = self.PCs[index + 1]        
    elif self.selected in self.NPCs:
      index = self.NPCs.index(self.selected)
      if index == len(self.NPCs) - 1: self.selected = None
      else:                           self.selected = self.NPCs[index + 1]
 
  def selectMouse(self):
    '''Select the nearest character under the mouse pointer.'''
    #self.selected = None
    buttons = [self.escape] + self.NPCs + self.PCs
    buttons.reverse()
    for button in buttons:
      if button.isMouseOver():
        self.selected = button
        break
 
  def chooseAction(self, entity):
    '''Escape, heal or attack the selected target.'''
    if not entity.isThinking(): return
    elif entity in self.NPCs: return
    elif self.selected == self.escape: entity.fear()
    elif self.selected in self.PCs:
      if entity.isHealer() and self.selected.isInjured():
        if self.selected == entity:
          entity.healSelf()
        else:
          entity.target = self.selected
          entity.headToHeal()
    elif self.selected in self.NPCs:
      if not(self.selected.isGone() or self.selected.isIncapacitated()):
        entity.target = self.selected
        entity.headToAttack()

 
  def input(self, entity):
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
        elif event.key == pygame.K_RETURN: self.chooseAction(entity)
      elif event.type == pygame.MOUSEMOTION: self.selectMouse()
      elif event.type == pygame.MOUSEBUTTONDOWN: self.chooseAction(entity)
    pygame.event.pump()

  def think(self, entity):
    '''Entities move and make decisions'''
    if entity.isThinking():
      if entity in self.NPCs: entity.randomAction(self.NPCs, self.PCs)
      #else:                   entity.randomAction(self.PCs, self.NPCs)
    for other_entity in self.PCs:  other_entity.move()
    for other_entity in self.NPCs: other_entity.move()

  def draw(self):
    '''Draw all the characters'''
    screen = pygame.display.get_surface()
    #screen.fill(WHITE)
    screen.blit(self.background.surface, (0,0))
    if self.selected in self.PCs:
      rect = self.heal.get_rect()
      rect.midbottom = self.selected.position
      rect.bottom = rect.bottom + 15
      screen.blit(self.heal, rect)
    elif self.selected in self.NPCs:
      rect = self.attack.get_rect()
      rect.midbottom = self.selected.position
      rect.bottom = rect.bottom + 15
      screen.blit(self.attack, rect)
    entities = self.PCs + self.NPCs
    entities.sort(lambda a, b: int(a.position[1] - b.position[1]))
    for entity in entities: entity.draw(screen)
    self.escape.draw(screen, self.selected == self.escape)
    pygame.display.flip()

  def turn(self, entity):
    '''One character's turn'''
    if entity.isIncapacitated() or entity.isGone(): return
    entity.startTurn()
    while not (self.quit or entity.isTurnOver()):
      self.input(entity)
      self.think(entity)
      self.draw()
      pygame.time.wait(self.delay)

  def loop(self):
    '''Take turns until the PCs or NPCs are defeated'''
    entities = self.sortedEntities()
    turn = 0
    while not self.quit:
      if isDefeated(self.PCs):  return
      if isDefeated(self.NPCs): return
      self.turn(entities[turn])
      turn = turn + 1
      if turn == len(entities): turn = 0

      
  