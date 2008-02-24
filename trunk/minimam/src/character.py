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

import random

# degrees of health
HEALTHY = 2
INJURED = 1
INCAPACITATED = 0

# stages of escape
STAYING = 0
LEAVING = 1
GONE = 2

class Character:

  '''Abstract base class for minimam Role-Playing Game characters.'''

  def __init__(self, level = 0):
    self.setLevel(level)
    self.health = HEALTHY
    self.escape = STAYING

  def __str__(self):
    '''
    Return a string representation of the Character.
    Automatically called when you add a Character to a string,
    and when you call str(x) where x is a Character.
    '''
    text = self.__class__.__name__
    text = "level " + self.getLevel() + " " + text
    if self.isHealthy():       text = "healthy " + text
    if self.isInjured():       text = "injured " + text
    if self.isIncapacitated(): text = "incapacitated " + text
    return text

  def __repr__(self):
    '''Return a string representation of the Character between "<" and ">"'''
    return "<" + self.__str() + ">"

  def getLevel(self):
    '''Return the character's current level.'''
    if self.character_points < 10:    return 0
    if self.character_points < 100:   return 1
    if self.character_points < 1000:  return 2
    if self.character_points < 10000: return 3
    return 4

  def setLevel(self, new_level):
    '''Set the character's level and give him the minimum CP for that level.'''
    self.character_points = pow(10, new_level)

  def roll(self):
    '''
    Simulate the value of rolling one six-sided die
    and adding the character's level.
    '''
    return random.randint(1,6) + self.getLevel()

  def attackRoll(self):
    return self.roll()

  def defenseRoll(self):
    return self.roll()

  def hideRoll(self):
    return self.roll()

  def takeNormalDamage(self):
    '''Be injured or incapacitated by a normal attack.'''
    self.escape = STAYING
    if self.isHealthy(): self.health = INJURED
    else:                self.health = INCAPACITATED

  def takeFireballDamage(self):
    '''Be incapacitated by a Wizard or Dragon's fireball.'''
    self.escape = STAYING
    self.health = INCAPACITATED

  def heal(self):
    '''Be healed.'''
    if self.isIncapacitated(): self.health = INJURED
    else:                      self.health = HEALTHY

  def attack(self, other):
    '''
    Try to attack another character.
    Returns True if the attack is successful, False if it fails.
    '''
    if self.attackRoll() > other.defenseRoll():
      other.takeNormalDamage()
      return True
    else:
      return False
  
  def restore(self):
    '''Remove temporary conditions such as damage and escaping.'''
    self.health = HEALTHY
    self.escape = STAYING

  def startEscaping(self):
    '''Call this when the character starts to escape.'''
    self.escape = LEAVING

  def finishEscaping(self):
    '''Call this when the character has been escaping for a full round.'''
    self.escape = GONE
    
  def isEscaping(self):
    return self.escape == LEAVING

  def isGone(self):
    return self.escape == GONE

  def isInjured(self):
    return self.health == INJURED
      
  def isIncapacitated(self):
    return self.health == INCAPACITATED

  def isHealthy(self):
    return self.health == HEALTHY

  def isHealer(self):
    return False

  def isFirst(self):
    return False

