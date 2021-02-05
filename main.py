from pygame import init 
from pygame.locals import QUIT
from pygame.display import set_caption, set_icon, set_mode, flip
from pygame.time import Clock
from pygame.draw import rect
from pygame.event import get
from pygame.image import load
from pygame.key import get_pressed
from pygame.sprite import Group
import pygame
from Player import Player
from game_const import SIZE, TITLE, ICON_PATH, COLOR, FPS

init()

clock = Clock()

screen = set_mode(SIZE)
set_caption(TITLE)
set_icon(load(ICON_PATH))

pl = Player(50, 50, (255, 255, 255))

all_sprites = Group()
all_sprites.add(pl)

running = True
while running:
  for event in get():
      if event.type == QUIT:
          running = False

  pressed_keys = get_pressed()

  pl.update(pressed_keys)

  screen.fill(COLOR)

  for s in all_sprites:
    screen.blit(s.surf, s.rect)

  flip()

  clock.tick(FPS)