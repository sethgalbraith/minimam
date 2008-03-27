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

import pygame

class Button:
  
  '''A clickable combat option'''
  
  def __init__(self, area):
    self.area = pygame.Rect(area) # the clickable area
      
  def isMouseOver(self):
    x, y = pygame.mouse.get_pos()
    return self.area.collidepoint(x, y)
  
    
    
    