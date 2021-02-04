from typing import Tuple
from pygame.draw import rect

GRAVITY = 9.8
VEL_Y = 0

class Player:
  def __init__(self, screen, x_vel: int, y_vel: int, width: int, height: int, color: Tuple[int, int, int]):
    self.screen = screen
    self.vel_x, self.vel_y = (x_vel, y_vel)
    self.mov_x, self.mov_y = (0, 0)
    VEL_Y = self.vel_y
    self.color = color
    self.rect = rect(screen, color, [0, 550, width, height])
    #self.sprite = load(pathImage)

  def draw(self):
    rect(self.screen, self.color, self.rect)

  def move_x(self):
    self.rect = self.rect.move(self.vel_x * self.mov_x, 0)
  
  def move_y(self):
    if self.mov_y == 0: return
    _, y_sc = self.screen.get_size()
    self.vel_y -= (self.mov_y * GRAVITY)
    print(self.vel_y)
    if self.rect.bottom - self.vel_y > y_sc: 
      self.mov_y = 0
      self.vel_y = VEL_Y
      self.rect.move_ip(0, y_sc - self.rect.height)
      return
    self.rect = self.rect.move(0, -self.vel_y)
    # print(y_sc)
    # if y_sc < self.rect.bottom: 

    #   x = self.rect.x
    #   y = y_sc - self.rect.height
    #   self.rect.move_ip(x, y)
    # print(f"{self.rect.x} {self.rect.y}")