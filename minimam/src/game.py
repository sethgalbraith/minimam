from warrior.py import Warrior
from rogue.py   import Rogue
from wizard.py  import Wizard
from priest.py  import Priest
from monster.py import Monster
from dragon.py  import Dragon
from character.py import *

def separateActiveCharacters(characters):
  """
  Find all characters in the list who are still fighting,
  separating Rogues and Dragons from other characters.
  """
  slow = []
  fast = []
  for ch in characters:
    if ch.health == INCAPACITATED or ch.escape == GONE: continue
    if issubclass(ch, Rogue): fast.append(character)
    else:                     slow.append(character)
  return fast, slow

def alternateTurns(first, second):
  """
  Combine lists, alternating items from 1st and 2nd list when possible.
  """
  turns = []
  # add as many alternating pairs as possible
  pairs = zip(first, second)
  for pair in pairs: turns += pair
  # add the remaining unpaired items from either list
  if len(pairs) < len(first): turns += first[len(pairs):]
  if len(pairs) < len(second): turns += second[len(pairs):]
  return turns

NO_WINNER = 0
PC_WINNER = 1
NPC_WINNER = 2

class Game:

  def __init__(self):
    self.PCs  = [] # player characters
    self.NPCs = [] # non-player characters
    self.sorted_characters = []
    self.turn = 0
    self.winner = NO_WINNER

  def startCombatRound(self):

    self.turn = 0

    # Combine the PC and NPC lists in the order of the character's turns.

    fastPCs,  slowPCs   = separateActiveCharacters(self.PCs)
    fastNPCs, slowNPCs  = separateActiveCharacters(self.NPCs)
    fastCharacters = alternateTurns(fastPCs, fastNPCs)
    slowCharacters = alternateTurns(slowPCs, slowNPCs)
    self.sorted_characters = fastCharacters + slowCharacters

    # If the combined list contains only PCs or NPCs determine who won.

    if len(fastPCs) == 0 and len(slowPCs) == 0:
      self.winner = NPC_WINNER
    elif len(fastNPCs) == 0 and len(slowNPCs) == 0:
      self.winner = PC_WINNER
    else:
      self.winner = NO_WINNER

  def getHealingTargets(self):
    """
    Get a list of all allies who are not healthy or escaping.
    """
    ch = self.sorted_characters[self.turn]
    if ch in PCs: allies = PCs
    else:         allies = NPCs
    targets = []
    for ally in allies:
      if ally.escape == STAYING and ally.health != HEALTHY:
        targets.append(ally)
    return targets

  def getAttackTargets(self):
    """
    Get a list of all enemies who are not incapacitated or gone.
    """
    ch = self.sorted_characters[self.turn]
    if ch in PCs: enemies = NPCs
    else:         enemies = PCs
    targets = []
    for enemy in enemies:
      if enemy.escape != GONE and enemy.health != INCAPACITATED:
        targets.append(enemy)
    return targets

  def performAction(self):
    """
    Heal or attack a random target.
    """
    ch = self.sorted_characters[self.turn]
    if issubclass(ch, Priest):
      targets = self.getHealingTargets()
      if len(targets > 0):
        random.choice(targets).heal()
        return
    targets = self.getAttackTargets()
    if len(targets > 0):
      ch.attack(random.choice(targets))

  def combatLoop(self):
    self.startCombatRound()
    while self.winner == NO_WINNER:
      self.performAction()
      self.turn += 1
      if self.turn == len(sorted_characters):
        self.startCombatRound()


if __name__ == "__main__":
  
  game = Game()

  game.PCs.append(Rogue())
  game.PCs.append(Warrior())
  game.PCs.append(Priest())
  game.PCs.append(Wizard())

  game.NPCs.append(Monster())
  game.NPCs.append(Dragon())
  game.NPCs.append(Monster())

  game.combatLoop()
