import pygame

RESOLUTION = 1200, 900
WHITE = 255, 255, 255

pygame.init()

screen = pygame.display.set_mode(RESOLUTION)

healthy = pygame.image.load("full-body-man-healthy.png")
injured = pygame.image.load("full-body-man-injured.png")
dead    = pygame.image.load("full-body-man-dead.png")

damage = 0

def refreshView():
  global damage
  screen.fill(WHITE)
  if damage == 0:
    image = healthy
  elif damage == 1:
    image = injured
  else:
    image = dead
  x = screen.get_rect().width
  x -= image.get_rect().width
  x = x / 2
  y = screen.get_rect().height
  y -= image.get_rect().height
  y = y / 2
  screen.blit(image, (x, y))
  pygame.display.flip()

def mainLoop():
  global damage
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          return
        if event.key == pygame.K_SPACE:
          damage = damage + 1
          if damage > 2:
            damage = 0
    pygame.event.pump()
    refreshView()
    pygame.time.wait(10)

mainLoop()
