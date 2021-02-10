# region Imports

from pygame.constants import KEYUP, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_w, K_z, K_x
from custom_udp import UDP_P2P
from pygame.display import set_caption, set_icon, set_mode, flip
from game_const import SIZE, TITLE, ICON_PATH, COLOR, FPS
from pygame.key import get_pressed
from pygame.sprite import Group
from pygame.locals import QUIT
from pygame.image import load
from pygame.time import Clock
from pygame.event import get
from Player import Attack, Player
from pygame import init

# endregion


def snd(keys):
    msg = str(
        {
            K_LEFT: keys[K_LEFT],
            K_RIGHT: keys[K_RIGHT],
            K_UP: keys[K_UP],
            K_a: keys[K_a],
            K_d: keys[K_d],
            K_w: keys[K_w],
            K_z: keys[K_z],
            K_x: keys[K_x],
        }
    )
    udp.transmission("CBG", "01", "CeF", msg)


def rcv(data, addr, port):
    if running:
        keys = eval(data.msg)
        pl2.update(keys)


def rcvErr(e):
    pass


init()

clock = Clock()

screen = set_mode(SIZE)
set_caption(TITLE)
set_icon(load(ICON_PATH))

udp = UDP_P2P("192.168.192.67", 6000, 6000)

all_sprites = Group()

pl = Player(50, 50, (255, 0, 0), 100, all_sprites)
plH = HealthBar(pl, pl.health, 10, 10)
pl2 = Player(50, 50, (0, 0, 255), 100, all_sprites)
pl2H = HealthBar(pl2, pl2.health, SIZE[0] - 110, 10)
all_sprites.add(pl, plH, pl2H)

rcvT = udp.receptionThread(rcv, rcvErr)
rcvT.start()

running = True
while running:
    for event in get():
        if event.type == QUIT:
            running = False

    pressed_keys = get_pressed()
    snd(pressed_keys)

    all_sprites.update(pressed_keys)

    screen.fill(COLOR)

    for s in all_sprites:
        screen.blit(s.surf, s.rect)

    screen.blit(pl2.surf, pl2.rect)

    flip()
    clock.tick(FPS)
