from character import Character

class Warrior(Character):

  def attackRoll(self):
    return self.roll() + 1

  def defenseRoll(self):
    return self.roll() + 1
