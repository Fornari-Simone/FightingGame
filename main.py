# region Imports

from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_w, K_z, K_x
from custom_udp import UDP_P2P
from pygame.display import set_caption, set_icon, set_mode, flip
from game_const import Color, Game
from pygame.key import get_pressed
from pygame.sprite import Group
from pygame.locals import QUIT
from pygame.image import load
from pygame.time import Clock
from pygame.event import get
from Player import Vegeth, Ichigo, Player
from HealthBar import HealthBar
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

screen = set_mode(Game.SIZE)
set_caption(Game.TITLE)
set_icon(load(Game.ICON_PATH))

udp = UDP_P2P("192.168.192.67", 6000, 6000)

all_sprites = Group()

pl = Ichigo(100, all_sprites)
plH = HealthBar(pl, 100, 10, 10)
# pl2 = Ichigo(100, all_sprites)
# pl2H = HealthBar(pl2, 100, Game.SIZE[0] - 110, 10)
all_sprites.add(pl)

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
    plH.update(pressed_keys)
    # pl2H.update(pressed_keys)

    screen.fill(Color.BLACK)

    all_sprites.draw(screen)

    # for s in all_sprites:
    #     screen.blit(s.surf, s.rect)

    screen.blit(plH.surfBg, plH.rectBg)
    screen.blit(plH.surfBar, plH.rectBar)
    # screen.blit(pl2H.surfBg, pl2H.rectBg)
    # screen.blit(pl2H.surfBar, pl2H.rectBar)
    # screen.blit(pl2.image, pl2.rect)

    flip()
    clock.tick(Game.FPS)