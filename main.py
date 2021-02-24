# region Imports

try:
    import pygame
except ImportError:
    import os

    os.system("python -m pip install pygame")

from pygame.display import set_caption, set_icon, set_mode, flip
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_z, K_x
from game.player.Player import Ichigo, Player, Vegeth
from game.const import Color, Game
from pygame.transform import scale
from udp.custom_udp import UDP_P2P
from pygame.key import get_pressed
from game.MainMenu import MainMenu
from pygame.sprite import Group
from pygame.locals import QUIT
from udp.packet import Packet
from pygame.image import load
from pygame.time import Clock
from pygame import init, quit
from pygame.event import get
from typing import Sequence
from game.Chat import Chat

# endregion

init()
gamestate = False


def sndKeys(nick: str, keys: Sequence, udp: UDP_P2P) -> None:
    # region DocString
    """
    Function to send the pressed keys

    ### Arguments
        `nick {str}`:
            `summary`: the username of the sender
        `keys {Sequence}`:
            `summary`: a dictionary with the status of all keys
        `udp {UDP_P2P}`:
            `summary`: the udp object
    """
    # endregion

    msg = str(
        {
            K_LEFT: keys[K_LEFT],
            K_RIGHT: keys[K_RIGHT],
            K_UP: keys[K_UP],
            K_z: keys[K_z],
            K_x: keys[K_x],
        }
    )
    udp.transmission(Game.APP, Game.VERSION, nick, msg)


def snd(nick: str, msg: str, udp: UDP_P2P) -> None:
    # region DocString
    """
    Function to send a string message

    ### Arguments
        `nick {str}`:
            `summary`: the username of the sender
        `msg {str}`:
            `summary`: the message to send
        `udp {UDP_P2P}`:
            `summary`: the udp object
    """
    # endregion

    udp.transmission(Game.APP, Game.VERSION, nick, msg)


def rcv(pl: Player, data: Packet, addr: str, port: int, time, chat) -> None:
    # region DocString
    """
    Function to receive data.
    If the message is 'Lost' or 'Quit' the gamestate is updated, otherwise the pressed keys\n
    are received and so the remote player is updated

    ### Arguments
        `pl {Player}`:
            `summary`: the destination's player object
        `data {Packet}`:
            `summary`: the data received
        `addr {str}`:
            `summary`: the address of the source of the data
        `port {int}`:
            `summary`: the port of the source of the data
    """
    # endregion

    global gamestate

    if data.app == "CHA":
        chat.__receive(data, addr, time)
    elif data.app == "CBG":
        if data.msg == "Lost":
            gamestate = "Win"
        elif data.msg == "Quit":
            gamestate = "Quitted"
        else:
            keys = eval(data.msg)
            pl.update(keys)


def rcvErr(e: Exception) -> None:
    # region DocString
    """
    Function that handle errors in the receive thread

    ### Arguments
        `e {Exception}`:
            `summary`: the exception to handle
    """
    # endregion

    print(e)


def gameloop(
    playerOrder: bool, p1Char: str, nick1: str, p2Char: str, nick2: str, udp: UDP_P2P
) -> str:
    # region DocString
    """
    Function that starts the loop for pygame

    ### Arguments
        `playerOrder {bool}`:
            `summary`: true if this host is the first player, false otherwise
        `p1Char {str}`:
            `summary`: the character chosen by this host
        `nick1 {str}`:
            `summary`: the username of this host
        `p2Char {str}`:
            `summary`: the character chosen by the remote player
        `nick2 {str}`:
            `summary`: the username of the remote player
        `udp {UDP_P2P}`:
            `summary`: the udp object

    ### Returns
        `str`: the exit status. It can be 'Lost' if this host lose, 'Quit' if this host closed the window,\n
        'Win' if the remote host lose, 'Quitted' if the remote host closed the window
    """
    # endregion

    global gamestate
    clock = Clock()

    # region Screen setup

    screen = set_mode(Game.SIZE)
    set_caption(Game.TITLE)
    set_icon(load(Game.ICON_PATH))
    bg = load(Game.BG_PATH).convert_alpha()
    bg = scale(bg, Game.SIZE)

    # endregion

    all_sprites = Group()

    # region Players setup

    if p1Char == "Ichigo":
        pl = Ichigo(playerOrder, nick1, all_sprites)
    elif p1Char == "Vegeth":
        pl = Vegeth(playerOrder, nick1, all_sprites)

    if p2Char == "Ichigo":
        pl2 = Ichigo(not playerOrder, nick2, all_sprites)
    elif p2Char == "Vegeth":
        pl2 = Vegeth(not playerOrder, nick2, all_sprites)

    # endregion

    chat = Chat(udp.ipDest, nick2, udp)

    rcvT = udp.receptionThread(
        lambda data, addr, port, time: rcv(pl2, data, addr, port, time, chat), rcvErr
    )
    rcvT.start()

    while True:

        # region Handle window close

        for event in get():
            if event.type == QUIT:
                snd(nick1, "Quit", udp)
                gamestate = "Quit"

        # endregion

        # region Handle key press and update sprites

        pressed_keys = get_pressed()
        sndKeys(nick1, pressed_keys, udp)
        all_sprites.update(pressed_keys)
        if pl.update(pressed_keys):
            snd(nick1, "Lost", udp)
            gamestate = "Lost"

        # endregion

        # region Sprite drawing

        screen.fill(Color.WHITE)
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        pl.draw(screen)
        pl2.draw(screen)
        pl.health.draw(screen)
        pl2.health.draw(screen)

        # endregion

        flip()
        clock.tick(Game.FPS)

        if gamestate:
            udp.stopThread()
            quit()
            return gamestate


if __name__ == "__main__":
    MainMenu(gameloop)
