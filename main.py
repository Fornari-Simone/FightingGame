# region Imports

from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_w, K_z, K_x
from pygame.transform import scale
from custom_udp import UDP_P2P
from pygame.display import set_caption, set_icon, set_mode, flip
from game_const import Color, Game
from pygame.key import get_pressed
from pygame.sprite import Group
from pygame.locals import QUIT
from pygame.image import load
from pygame.time import Clock
from pygame.event import get
from Player import Ichigo, Vegeth
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
bg = load(Game.BG_PATH).convert_alpha()
bg = scale(bg, Game.SIZE)

udp = UDP_P2P("192.168.192.67", 6000, 6000)

all_sprites = Group()

pl = Ichigo(True, all_sprites)
pl2 = Vegeth(False, all_sprites)
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

    screen.fill(Color.WHITE)
    screen.blit(bg, (0, 0))

    all_sprites.draw(screen)
    pl2.draw(screen)

    pl.health.draw(screen)
    pl2.health.draw(screen)

    flip()
    clock.tick(Game.FPS)