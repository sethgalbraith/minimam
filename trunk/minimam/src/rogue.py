from character.py import *

class Rogue(Character):

  def hideRoll(self):
    return self.roll() + 1

  def defenseRoll(self):
    if self.escape == LEAVING:
      return self.roll() + 1
    else:
      return self.roll()
