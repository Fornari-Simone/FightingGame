# region Imports

from pygame.display import set_caption, set_icon, set_mode, flip
from game_const import SIZE, TITLE, ICON_PATH, COLOR, FPS
from pygame.key import get_pressed
from pygame.sprite import Group
from pygame.locals import QUIT
from pygame.image import load
from pygame.time import Clock
from pygame.event import get
from Player import Player
from pygame import init

# endregion

init()

clock = Clock()

screen = set_mode(SIZE)
set_caption(TITLE)
set_icon(load(ICON_PATH))


all_sprites = Group()

pl = Player(50, 50, (255, 255, 255), all_sprites)
all_sprites.add(pl)

running = True
while running:
    for event in get():
        if event.type == QUIT:
            running = False

    pressed_keys = get_pressed()

    all_sprites.update(pressed_keys)

    screen.fill(COLOR)

    for s in all_sprites:
        screen.blit(s.surf, s.rect)

    flip()
    clock.tick(FPS)
