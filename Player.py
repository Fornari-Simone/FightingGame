from typing import Tuple
from pygame.draw import rect
class Player:
  def __init__(self, screen, vel: x_vel: int, y_vel: int x: int, y: int, width: int, height: int, 
    color: Tuple[int, int, int]):
    self.gravity = 9.8
    self.vel = (x_vel, y_vel)
    self.color = color
    self.rect = rect(screen, color, [x, y, width, height])
    #self.sprite = load(pathImage)

  def draw(screen):
    