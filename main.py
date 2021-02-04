from pygame import init, KEYDOWN, KEYUP, K_LEFT, K_a, K_RIGHT, K_d, K_UP, K_w, QUIT
from pygame.display import set_caption, set_icon, set_mode, update
from pygame.draw import rect
from pygame.event import get
from pygame.image import load
import pygame
from Player import Player

# WIDTH, HEIGHT
SIZE = (600, 600)
# RED, GREEN, BLUE
COLOR = (0, 0, 0)
TITLE = "Fighting Game"
ICON_PATH = "img/GameIcon.png"

init()

screen = set_mode(SIZE)
set_caption(TITLE)
set_icon(load(ICON_PATH))

pl = Player(screen, 1, 15, 50, 50, (255, 255, 255))
run = True
while run:
  for event in get():
    if event.type == QUIT: run = False
    elif event.type == KEYDOWN:
      if event.key == K_a or event.key == K_LEFT:
        pl.mov_x = -1
      elif event.key == K_d or event.key == K_RIGHT:  
        pl.mov_x = 1
      elif event.key == K_w or event.key == K_UP:
        pl.mov_y = 0.1
    elif event.type == KEYUP:
      if (event.key == K_a or 
          event.key == K_LEFT or
          event.key == K_d or
          event.key == K_RIGHT):
        pl.mov_x = 0
  
  screen.fill(COLOR)
  pl.move_x()
  pl.move_y()
  pl.draw()
  #pygame.Rect.move_ip(pl.rect, 0, 50)
  update()
