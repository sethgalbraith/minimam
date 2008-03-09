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

from warrior   import Warrior
from rogue     import Rogue
from wizard    import Wizard
from priest    import Priest
from monster   import Monster
from dragon    import Dragon
from entity    import Entity

import pygame
import random

WHITE = 255, 255, 255

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

class Game:

  def __init__(self):
    self.PCs  = [] # player characters
    self.NPCs = [] # non-player characters
    self.quit = False
    self.width = 640       # screen width
    self.height = 480      # screen height
    self.delay = 10        # duration of animation frames in milliseconds
    self.speed = 10        # distance moved by characters each turn
    self.horizontal_spacing = 200
    self.vertical_spacing   = 100
    self.center = 320, 240 # middle of the battlefield for all characters
    self.edge = 100        # distance from edge of screen to escape goal
    self.push = 100        # distance a character gets pushed by an attack

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
          if self.screen.get_flags() & pygame.FULLSCREEN:
            pygame.display.set_mode((self.width, self.height))
          else:
            pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
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
    #self.screen.fill(WHITE)
    self.screen.blit(self.background, (0,0))
    entities = self.PCs + self.NPCs
    entities.sort(lambda a, b: int(a.position[1] - b.position[1]))
    for entity in entities:  entity.draw(self.screen)
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

  def fight(self):
    '''Take turns until the PCs or NPCs are defeated'''
    entities = self.sortedEntities()
    turn = 0
    for i in range(len(self.PCs)):
      self.PCs[i].startCombat(i, len(self.PCs), False)
    for i in range(len(self.NPCs)):
      self.NPCs[i].startCombat(i, len(self.NPCs), True)
    while not self.quit:
      if isDefeated(self.PCs):  return
      if isDefeated(self.NPCs): return
      self.turn(entities[turn])
      turn = turn + 1
      if turn == len(entities): turn = 0

  def explore(self):
    '''Explore the map'''
    # FIXME: create the exploration part of game
    while not self.quit:
      self.randomParty()
      self.fight()
      if   isDefeated(self.PCs):  print "NPCs won!"
      elif isDefeated(self.NPCs): print "PCs won!"
      else:                       print "Who won?"
      for entity in self.PCs:  entity.character.restore()
      for entity in self.NPCs: entity.character.restore()          

  def start(self):
    '''Begin the game'''
    pygame.init()
    for resolution in RESOLUTIONS:
      if pygame.display.mode_ok(resolution, pygame.FULLSCREEN):
        self.width, self.height = resolution
        break
    self.screen = pygame.display.set_mode((self.width, self.height),
                                          pygame.FULLSCREEN)
    self.center = 0.50 * self.width, self.height - self.vertical_spacing
    self.background = pygame.image.load('All_Gizah_Pyramids-cropped.jpg')
    self.background = pygame.transform.scale(self.background, (self.width, self.height))
    self.background = self.background.convert()
    self.explore()

  def randomParty(self):
    choice = random.randrange(2)
    #choice = 1
    if choice == 0:
      self.PCs  = []
      self.PCs.append(Entity(Warrior(), self))
      self.PCs.append(Entity(Warrior(), self))
      self.PCs.append(Entity(Warrior(), self))
      self.NPCs = []
      self.NPCs.append(Entity(Rogue(),  self))
      self.NPCs.append(Entity(Rogue(),  self))
      self.NPCs.append(Entity(Rogue(),  self))
      self.NPCs.append(Entity(Rogue(),  self))
    if choice == 1:
      self.PCs  = []
      self.PCs.append(Entity(Rogue(),   self))
      self.PCs.append(Entity(Warrior(), self))
      self.PCs.append(Entity(Rogue(),   self))
      self.PCs.append(Entity(Warrior(), self))
      self.PCs.append(Entity(Rogue(),   self))
      self.NPCs = []
      self.NPCs.append(Entity(Dragon(), self))
      #self.NPCs[-1].character.setLevel(1)
      self.NPCs.append(Entity(Dragon(), self))
      #self.NPCs[-1].character.setLevel(1)

if __name__ == "__main__":
  
  game = Game()
  game.start()