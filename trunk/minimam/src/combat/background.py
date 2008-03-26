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

class Background:
  
  def __init__(self, filename):
    '''Create a background from an image file stretched to fill the screen.'''
    screen = pygame.display.get_surface()
    self.surface = pygame.image.load(filename)
    self.surface = pygame.transform.scale(self.surface, screen.get_size())
    self.surface = self.surface.convert()

  def draw(self):
    '''Draw the background on the screen.'''
    screen = pygame.display.get_surface()
    screen.blit(self.surface, (0, 0))
    