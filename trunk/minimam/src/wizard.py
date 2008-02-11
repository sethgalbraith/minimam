from character.py import *

class Wizard(Character):

  def attack(self, other):
    if self.attackRoll() > other.defenseRoll():
      other.takeFireballDamage()
      return True
    else:
      return False
