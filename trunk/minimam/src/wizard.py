from character import Character

class Wizard(Character):

  def attack(self, other):
    if self.attackRoll() > other.defenseRoll():
      other.takeFireballDamage()
      return True
    else:
      return False
