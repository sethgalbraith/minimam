from warrior   import Warrior
from rogue     import Rogue
from wizard    import Wizard
from priest    import Priest
from monster   import Monster
from dragon    import Dragon
from entity    import Entity
from animation import Animation

import pygame

WIDTH, HEIGHT = 1200, 900
DELAY = 10
WHITE = 255, 255, 255

NO_WINNER = 0
PC_WINNER = 1
NPC_WINNER = 2

def separateByStatusAndClass(entities):
  '''
  Find all characters in the list who are still fighting,
  separating Rogues and Dragons from other characters.
  '''
  slow = []
  fast = []
  for each_entity in entities:
    if each_entity.isIncapacitated(): continue
    if each_entity.isGone():          continue
    if each_entity.goesFirst(): fast.append(each_entity)
    else:               slow.append(each_entity)
  return fast, slow

def alternateTurns(first, second):
  '''Combine lists, alternating items from 1st and 2nd list when possible.'''
  turns = []
  # add as many alternating pairs as possible
  pairs = zip(first, second)
  for pair in pairs: turns += pair
  # add the remaining unpaired items from either list
  if len(pairs) < len(first): turns += first[len(pairs):]
  if len(pairs) < len(second): turns += second[len(pairs):]
  return turns

class Game:

  def __init__(self):
    self.PCs  = [] # player characters
    self.NPCs = [] # non-player characters
    self.sorted_entities = []
    self.turn = 0
    self.winner = NO_WINNER
    self.quit = False

  def startCombatRound(self):
    '''Sort the entities by team and status and check victory conditions'''
    self.turn = 0
    # Combine the PC and NPC lists in the order of the character's turns.
    fastPCs,  slowPCs  = separateByStatusAndClass(self.PCs)
    fastNPCs, slowNPCs = separateByStatusAndClass(self.NPCs)
    fast = alternateTurns(fastPCs, fastNPCs)
    slow = alternateTurns(slowPCs, slowNPCs)
    self.sorted_entities = fast + slow
    # If the combined list contains only PCs or NPCs determine who won.
    if   len(fastPCs)  == 0 and len(slowPCs)  == 0: self.winner = NPC_WINNER
    elif len(fastNPCs) == 0 and len(slowNPCs) == 0: self.winner = PC_WINNER
    else:                                           self.winner = NO_WINNER

  def processEvents(self):
    for event in pygame.event.get():
      if event == pygame.QUIT:
        self.quit = True
    pygame.event.pump()

  def turnLoop(self):
    current_entity = self.sorted_entities[self.turn]
    current_entity.startTurn()
    while not (self.quit or current_entity.isTurnOver()):
      self.processEvents()
      if current_entity in PCs: allies, enemies = PCs, NPCs
      else:                     allies, enemies = NPCs, PCs
      current_entity.randomAction(allies, enemies)
      self.screen.fill(WHITE)
      all_entities = PCs + NPCs
      for each_entity in all_entities: each_entity.move()
      for each_entity in all_entities: each_entity.draw(self.screen)
      pygame.display.flip()
      pygame.time.wait(DELAY)

  def combatLoop(self):
    '''Take turns until the PCs or NPCs are defeated'''
    self.startCombatRound()
    while self.winner == NO_WINNER and not self.quit:
      self.turnLoop()
      self.turn += 1
      if self.turn == len(sorted_characters):
        self.startCombatRound()

  def start(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    self.combatLoop()
    if   self.winner ==  PC_WINNER: print "PCs won!"
    elif self.winner == NPC_WINNER: print "NPCs won!"
    else:                           print "Who won?"

# store animations for each class in a dictionary
# so we don't have to duplicate frames for each character
animations = {}
for classname in "rogue", "warrior", "priest", "wizard", "monster", "dragon":
  animations[classname] = Animation(classname)

if __name__ == "__main__":
  
  game = Game()

  game.PCs.append(Entity(Rogue(),   animations["rogue"]))
  game.PCs.append(Entity(Warrior(), animations["warrior"]))
  game.PCs.append(Entity(Priest(),  animations["priest"]))
  game.PCs.append(Entity(Wizard(),  animations["wizard"]))

  game.NPCs.append(Entity(Monster(), animations["monster"]))
  game.NPCs.append(Entity(Dragon(),  animations["dragon"]))
  game.NPCs.append(Entity(Monster(), animations["monster"]))

  game.start()
