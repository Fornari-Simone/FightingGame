from pygame_gui.elements.ui_label import UILabel
from game.const import Game, Color
from pygame.display import set_caption, set_icon, set_mode, flip
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_z, K_x
from pygame.transform import scale
from pygame.key import get_pressed
from pygame.sprite import Group
from pygame.locals import QUIT
from pygame.image import load
from pygame.time import Clock
from pygame import init, quit, Rect, USEREVENT
from pygame.event import get
from pygame_gui import UIManager, UI_BUTTON_PRESSED, UI_TEXT_ENTRY_FINISHED
from pygame_gui.elements import UITextBox, UITextEntryLine, UIButton, UIScrollingContainer

init()

clock = Clock()

screen = set_mode((Game.SIZE[0] + 400, Game.SIZE[1]))
set_caption(Game.TITLE)
set_icon(load(Game.ICON_PATH))
bg = load(Game.BG_PATH).convert_alpha()
bg = scale(bg, Game.SIZE)

manager = UIManager((Game.SIZE[0] + 400, Game.SIZE[1]))

cont = UIScrollingContainer(relative_rect=Rect((Game.SIZE[0], 0), (400, Game.SIZE[1] - 50)),manager=manager)
ins = UITextEntryLine(
    relative_rect=Rect((Game.SIZE[0], Game.SIZE[1] - 50), (350, 50)), manager=manager
)
enter = UIButton(
    text="Enter",
    relative_rect=Rect((Game.SIZE[0] + 350, Game.SIZE[1] - 50), (50, 50)),
    manager=manager,
)

msgs = []


run = True
while run:
    dt = clock.tick(Game.FPS) / 1000.0
    pressed_keys = get_pressed()

    for event in get():
        if event.type == QUIT:
            quit()
            run = False

        if event.type == USEREVENT:
            if event.user_type == UI_BUTTON_PRESSED:
                if event.ui_element == enter:
                    cont.get_container().add_element(UILabel(relative_rect=Rect((0, 0),(100, 100)), manager=manager))
            if event.user_type == UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == ins:
                    pass

        manager.process_events(event)

    manager.update(dt)

    screen.fill(Color.WHITE)
    screen.blit(bg, (0, 0))

    manager.draw_ui(screen)

    flip()
