from enum import Enum

class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

class Physics:
    GRAVITY = 9.8
    VEL_Y = 5
    VEL_X = 5
    
class Game:
	ICON_PATH = "img/GameIcon.png"
	TITLE = "Fighting Game"
	SIZE = (600, 600)
	FPS = 60
