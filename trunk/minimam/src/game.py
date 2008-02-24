from warrior   import Warrior
from rogue     import Rogue
from wizard    import Wizard
from priest    import Priest
from monster   import Monster
from dragon    import Dragon
from entity    import Entity

import pygame

WIDTH, HEIGHT = 1200, 800
DELAY = 10
WHITE = 255, 255, 255

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
  # add as many alternating pairs as possible
  pairs = zip(first, second)
  for pair in pairs: turns = turns + pair
  # add the remaining unpaired items from either list
  if len(pairs) < len(first):
    turns = turns + first[len(pairs):]
  if len(pairs) < len(second):
    turns = turns + second[len(pairs):]
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
        self.quit = True
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
    self.screen.fill(WHITE)
    for entity in self.PCs:  entity.draw(self.screen)
    for entity in self.NPCs: entity.draw(self.screen)
    pygame.display.flip()

  def turn(self, entity):
    '''One character's turn'''
    if entity.isIncapacitated() or entity.isGone(): return
    entity.startTurn()
    while not (self.quit or entity.isTurnOver()):
      self.input()
      self.think(entity)
      self.draw()
      pygame.time.wait(DELAY)

  def fight(self):
    '''Take turns until the PCs or NPCs are defeated'''
    entities = self.sortedEntities()
    turn = 0
    for i in range(len(self.PCs)):
      self.PCs[i].setHome(i, len(self.PCs), False)
    for i in range(len(self.NPCs)):
      self.NPCs[i].setHome(i, len(self.NPCs), True)
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
      self.fight()
      if   isDefeated(self.PCs):  print "NPCs won!"
      elif isDefeated(self.NPCs): print "PCs won!"
      else:                       print "Who won?"
      for entity in self.PCs:  entity.character.restore()
      for entity in self.NPCs: entity.character.restore()          

  def start(self):
    '''Begin the game'''
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    self.explore()

if __name__ == "__main__":
  
  game = Game()

  game.PCs.append(Entity(Warrior()))
  game.PCs.append(Entity(Warrior()))
  game.PCs.append(Entity(Warrior()))

  game.NPCs.append(Entity(Rogue()))
  game.NPCs.append(Entity(Rogue()))
  game.NPCs.append(Entity(Rogue()))
  game.NPCs.append(Entity(Rogue()))

#  game.PCs.append(Entity(Rogue()))
#  game.PCs.append(Entity(Warrior()))
#  game.PCs.append(Entity(Priest()))
#  game.PCs.append(Entity(Wizard()))
#
#  game.NPCs.append(Entity(Monster()))
#  game.NPCs.append(Entity(Dragon()))
#  game.NPCs.append(Entity(Monster()))

  game.start()
