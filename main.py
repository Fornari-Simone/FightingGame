# region Imports

from MainMenu import MainMenu
from datetime import datetime
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_k, K_l, K_w, K_z, K_x
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

init()

IP = "79.56.131.174"


def snd(keys, udp):
    msg = str(
        {
            K_LEFT: keys[K_LEFT],
            K_RIGHT: keys[K_RIGHT],
            K_UP: keys[K_UP],
            K_z: keys[K_z],
            K_x: keys[K_x],
        }
    )
    udp.transmission("CBG", "01", "CeF", msg)


def rcv(pl, data, addr, port):
    keys = eval(data.msg)
    pl.update(keys)


def rcvErr(e):
    print("OH NO")
    pass


def gameloop(playerOrder, udp):
    clock = Clock()

    screen = set_mode(Game.SIZE)
    set_caption(Game.TITLE)
    set_icon(load(Game.ICON_PATH))
    bg = load(Game.BG_PATH).convert_alpha()
    bg = scale(bg, Game.SIZE)

    all_sprites = Group()

    pl = Ichigo(playerOrder, all_sprites)
    pl2 = Ichigo(not playerOrder, all_sprites)

    rcvT = udp.receptionThread(
        lambda data, addr, port: rcv(pl2, data, addr, port), rcvErr
    )
    rcvT.start()
    
    gameState = Game.INGAME
    while not gameState:
        for event in get():
            if event.type == QUIT:
                udp.stopThread()
                return

        pressed_keys = get_pressed()
        snd(pressed_keys, udp)
        all_sprites.update(pressed_keys)
        pl.update(pressed_keys)

        screen.fill(Color.WHITE)
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        pl.draw(screen)
        pl2.draw(screen)
        pl.health.draw(screen)
        pl2.health.draw(screen)

        flip()
        clock.tick(Game.FPS)


if __name__ == "__main__":
    # udp = UDP_P2P(IP, 6000, 6000)
    # """
	# 	p1      p2
	# 	on  -->  lose
	# 	get <--  on
		
	# """
    # while True:
    #     udp.transmission("CBG", "01", "cazzo", "connection")
    #     rdata, _, rtime = udp.singleReceive()
    #     if rdata.msg == "connection":
    #         udp.transmission("CBG", "01", "cazzo", "connection")
    #         stime = udp.transmission("CBG", "01", "cazzo", "player order")
    #         rdata, _, rtime = udp.singleReceive()
    #         if rdata.msg == "connection":
    #             rdata, _, rtime = udp.singleReceive()
    #         imPlayer1 = stime < datetime.strptime(rdata.time + "000", "%H%M%S%f")
    #         break

    # gameloop(imPlayer1, udp)
    MainMenu(gameloop)
