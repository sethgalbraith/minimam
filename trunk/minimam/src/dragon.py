from character.py import *

# Dragon inherits the advantages of all other classes.
# IMPORTANT NOTE: Warrior comes after Rogue
# because Warrior has better defenseRoll method.

class Dragon(Rogue, Warrior, Wizard, Priest):
  pass

  
