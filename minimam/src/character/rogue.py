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

from character import Character

class Rogue(Character):

  def hideRoll(self):
    return self.roll() + 1

  def attackRoll(self, other):
    if other.isEscaping():
      return self.roll() + 1
    else:
      return self.roll()

  def defenseRoll(self, other):
    if self.isEscaping():
      return self.roll() + 1
    else:
      return self.roll()

  def isFirst(self):
    return True
