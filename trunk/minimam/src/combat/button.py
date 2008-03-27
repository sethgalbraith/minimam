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

WHITE = 255, 255, 255
GRAY  = 64, 64, 64
BLACK = 0, 0, 0
CLEAR = 0, 0, 0, 0

SHADOW = 1, 2

class Button:
  
  '''A clickable combat option'''
  
  def __init__(self, name):
    path = "graphics/" + name
    self.surfaces = {
      True:  pygame.image.load("%s-selected.png" % path).convert_alpha(),
      False: pygame.image.load("%s.png" % path).convert_alpha()
    }
    self.rect = self.surfaces[False].get_rect()

  def isMouseOver(self):
    x, y = pygame.mouse.get_pos()
    return self.rect.collidepoint(x, y)
  
  def draw(self, screen, selected = False):
    screen.blit(self.surfaces[selected], self.rect)
    