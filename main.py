from pygame import init, QUIT
from pygame.display import set_caption, set_icon, set_mode, update
from pygame.draw import rect
from pygame.event import get
from pygame.image import load
#from Player import Player

# WIDTH, HEIGHT
SIZE = (800, 600)
# RED, GREEN, BLUE
COLOR = (0, 0, 0)
TITLE = "Fighting Game"
ICON_PATH = "img/GameIcon.png"

#pl = Player((0, 0),(0,0,50,50), (255, 255, 255))
init()

screen = set_mode(SIZE)
set_caption(TITLE)
set_icon(load(ICON_PATH))
rct = rect(screen, (255,255,255), [0,0,50,50])
run = True
while run:
  for event in get():
    if event.type == QUIT: run = False
  
  screen.fill(COLOR)
  rct = rect(screen, (255,255,255), rct)
  update()