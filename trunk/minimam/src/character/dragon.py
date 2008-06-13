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

#from warrior import Warrior
#from rogue   import Rogue
#from wizard  import Wizard
#from priest  import Priest
#
## Dragon inherits the advantages of all other classes.
## IMPORTANT NOTE: Warrior comes after Rogue
## because Warrior has better defenseRoll method.
#
#class Dragon(Rogue, Warrior, Wizard, Priest):
#  pass

from character import Character

class Dragon(Character):

  def hideRoll(self):
    return self.roll() + 1

  def isFirst(self):
    return True

  def attack(self, other):
    if self.attackRoll(other) > other.defenseRoll(other):
      other.takeFireballDamage()
      return True
    else:
      return False

  def attackRoll(self, other):
    return self.roll() + 1

  def defenseRoll(self, other):
    return self.roll() + 1

  def isHealer(self):
    return True
  
