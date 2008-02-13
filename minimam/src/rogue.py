from character import Character

class Rogue(Character):

  def hideRoll(self):
    return self.roll() + 1

  def defenseRoll(self):
    if self.isEscaping():
      return self.roll() + 1
    else:
      return self.roll()

  def isFirst(self):
    return True
