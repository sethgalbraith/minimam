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
    self.width, self.height = screen.get_size()
    self.ring = pygame.rect.Rect(0, 0, 600, 300) # combat circle
    self.ring.centerx = self.width / 2
    self.ring.bottom = self.height
    self.background = Background('graphics/All_Gizah_Pyramids-cropped.jpg')
    self.setPlayerCharacters(PCs)
    self.setNonPlayerCharacters(NPCs)
    self.quit = False
    
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
 
  def input(self):
    '''Respond to user interface events'''
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit = True
      if event.type == pygame.KEYDOWN:
        # Escape key quits
        if event.key == pygame.K_ESCAPE:
          self.quit = True
        # F11 toggles windowed and fullscreen
        if event.key == pygame.K_F11:
          screen = pygame.display.get_surface()
          if screen.get_flags() & pygame.FULLSCREEN:
            pygame.display.set_mode(screen.get_size())
          else:
            pygame.display.set_mode(screen.get_size(), pygame.FULLSCREEN)
    pygame.event.pump()

  def think(self, entity):
    '''Entities move and make decisions'''
    if entity.isThinking():
      if entity in self.PCs:
          allies, enemies = self.PCs, self.NPCs
      else:
          allies, enemies = self.NPCs, self.PCs
      entity.randomAction(allies, enemies)
    for other_entity in self.PCs:  other_entity.move()
    for other_entity in self.NPCs: other_entity.move()

  def draw(self):
    '''Draw all the characters'''
    screen = pygame.display.get_surface()
    #screen.fill(WHITE)
    screen.blit(self.background.surface, (0,0))
    entities = self.PCs + self.NPCs
    entities.sort(lambda a, b: int(a.position[1] - b.position[1]))
    for entity in entities:  entity.draw(screen)
    pygame.display.flip()

  def turn(self, entity):
    '''One character's turn'''
    if entity.isIncapacitated() or entity.isGone(): return
    entity.startTurn()
    while not (self.quit or entity.isTurnOver()):
      self.input()
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

      
  