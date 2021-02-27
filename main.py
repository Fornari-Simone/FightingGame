# region Imports

try:
    import pygame
except ImportError:
    import os

    os.system("python -m pip install pygame")
    import pygame

try:
    import pygame_gui
except ImportError:
    import os

    os.system("python -m pip install pygame_gui")
    import pygame_gui

from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_z, USEREVENT
from pygame.display import set_caption, set_icon, set_mode, flip
from game.player.Player import Ichigo, Player, Vegeth
from pygame.time import Clock, set_timer
from game.const import Color, Game
from pygame.transform import scale
from udp.custom_udp import UDP_P2P
from pygame.key import get_pressed
from game.MainMenu import MainMenu
from pygame_gui import UIManager
from pygame.sprite import Group
from pygame.locals import QUIT
from datetime import datetime
from udp.packet import Packet
from pygame.image import load
from pygame import init, quit
from pygame.event import get
from game.Chat import Chat

# endregion

init()
gamestate = False


def sndKeys(nick: str, keys: tuple[int, int, int, int], udp: UDP_P2P) -> None:
    # region DocString
    """
    Function to send the pressed keys

    ### Arguments
        `nick {str}`:
            `summary`: the username of the sender
        `keys {(int, int, int, int)}`:
            `summary`: a tuple with the status of the control keys
        `udp {UDP_P2P}`:
            `summary`: the udp object
    """
    # endregion

    msg = f"K{keys[0]},{keys[1]},{keys[2]},{keys[3]}"
    udp.transmission(Game.APP, Game.VERSION, nick, msg)


def sndCoords(nick: str, coords: tuple[int, int], udp: UDP_P2P) -> None:
    # region DocString
    """
    Function to send the coords of the player

    ### Arguments
        `nick {str}`:
            `summary`: the username of the sender
        `coords {(int, int, int, int)}`:
            `summary`: a tuple with the coords of the player
        `udp {UDP_P2P}`:
            `summary`: the udp object
    """
    # endregion

    msg = f"C{coords[0]},{coords[1]}"
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


def rcv(
    pl: Player, data: Packet, addr: tuple[str, int], time: datetime, chat: Chat
) -> None:
    # region DocString
    """
    Function to receive data.
    If the APP field is CBG and the message is 'Lost' or 'Quit' the gamestate is updated,\n
    if the APP field is CBG and the message begins with 'K' the pressed keys are sent to the player object,\n
    if the APP field is CBG and the message begins with 'C' the coords of the player are checked,\n
    if the APP field is CHA a chat message arrived

    ### Arguments
        `pl {Player}`:
            `summary`: the destination's player object
        `data {Packet}`:
            `summary`: the data received
        `addr {(str, int)}`:
            `summary`: the address and the port of the source of the data
        `time {datetime}`:
            `summary`: the time the data arrived
        `chat {Chat}`:
            `summary`: reference to the chat object
    """
    # endregion

    global gamestate

    if data.app == "CHA":
        chat.receive(data, addr, time)
    elif data.app == "CBG":
        if data.msg == "Lost":
            gamestate = "Win"
        elif data.msg == "Quit":
            gamestate = "Quitted"
        elif data.msg[0] == "K":
            d = data.msg[1:].split(",")
            keys = {
                K_LEFT: int(d[0]),
                K_RIGHT: int(d[1]),
                K_UP: int(d[2]),
                K_z: int(d[3]),
            }
            pl.update(keys)
        elif data.msg[0] == "C":
            d = data.msg[1:].split(",")
            coords = (int(d[0]), int(d[1]))
            if pl.rect.x != coords[0] or pl.rect.y != coords[1]:
                pl.reposition(coords)


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
    playerOrder: bool,
    p1Char: str,
    nick1: str,
    p2Char: str,
    nick2: str,
    udp: UDP_P2P,
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
    COORDSYNC = USEREVENT + 1
    set_timer(COORDSYNC, 1000)

    # region Screen setup

    screen = set_mode((Game.SIZE[0] + 400, Game.SIZE[1]))
    set_caption(Game.TITLE)
    set_icon(load(Game.ICON_PATH))
    bg = load(Game.BG_PATH).convert_alpha()
    bg = scale(bg, Game.SIZE)

    manager = UIManager((Game.SIZE[0] + 400, Game.SIZE[1]))
    chat = Chat((400, Game.SIZE[1]), manager, udp, nick1)

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

    rcvT = udp.receptionThread(
        lambda data, addr, time: rcv(pl2, data, addr, time, chat), rcvErr
    )
    rcvT.start()

    while True:

        dt = clock.tick(Game.FPS) / 1000

        # region Handle window close

        pressed_keys = get_pressed()

        for event in get():
            if event.type == QUIT:
                snd(nick1, "Quit", udp)
                gamestate = "Quit"

            if event.type == COORDSYNC:
                sndCoords(nick1, (pl.rect.x, pl.rect.y), udp)

            manager.process_events(event)

        # endregion

        manager.update(dt)

        # region Handle key press and update sprites

        all_sprites.update(pressed_keys)
        sndKeys(
            nick1,
            (
                pressed_keys[K_LEFT],
                pressed_keys[K_RIGHT],
                pressed_keys[K_UP],
                pressed_keys[K_z],
            ),
            udp,
        )
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

        manager.draw_ui(screen)
        flip()

        if gamestate:
            udp.stopThread()
            quit()
            return gamestate


if __name__ == "__main__":
    MainMenu(gameloop)
