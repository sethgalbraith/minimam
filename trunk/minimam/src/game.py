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


# To-do implement the exploration part of the game
# the following code is already in combat/fight.py
# and should be removed as soon as we have something else here

if __name__ == "__main__":
  
  from character.warrior import Warrior
  from character.rogue   import Rogue
  from character.wizard  import Wizard
  from character.priest  import Priest
  from character.monster import Monster
  from character.dragon  import Dragon
  
  from combat.fight import Fight
  
  import pygame
  import random
  
  RESOLUTIONS = [
    (1680, 1050), # WSXGA+
    (1600, 1200), # UXGA
    (1440, 900),  # ulrich's laptop
    (1400, 1050), # SXGA+
    (1280, 1024), # WXGA
    (1280, 800),  # my laptop
    (1200, 900),  # OLPC XO-1
    (1024, 768),  # XGA
    (800, 600),   # SVGA
    (800, 480),   # WVGA (Eee PC, CloudBook)
    (640, 480)]   # VGA
  
  pygame.init()
  for resolution in RESOLUTIONS:
    if pygame.display.mode_ok(resolution, pygame.FULLSCREEN):
      pygame.display.set_mode(resolution, pygame.FULLSCREEN)
      break
  pygame.mouse.set_visible(True)
  
  fight = Fight()
  while not fight.quit:
    choice = random.randrange(3)
    if choice == 0:
      PCs = [Warrior(), Warrior(), Warrior()]
      NPCs = [Rogue(), Rogue(), Rogue(), Rogue()]
    if choice == 1:
      PCs = [Rogue(), Warrior(), Rogue(), Warrior(), Rogue()]
      NPCs = [Dragon(), Dragon()]
    if choice == 2:
      PCs = [Priest(), Rogue(), Warrior(), Wizard()]
      for character in PCs: character.setLevel(1)
      NPCs = [Monster(), Monster(), Dragon(), Monster(), Monster()]
      NPCs[2].setLevel(2)
    fight.setPlayerCharacters(PCs)
    fight.setNonPlayerCharacters(NPCs)
    fight.loop()
