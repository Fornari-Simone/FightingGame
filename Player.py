from typing import Tuple
from pygame import Surface
from pygame.locals import KEYUP, K_LEFT, K_a, K_RIGHT, K_d, K_UP, K_w
from pygame.draw import rect
from pygame.sprite import Sprite
from pygame.locals import KEYDOWN, KEYUP, K_LEFT, K_a, K_RIGHT, K_d, K_UP, K_w, QUIT

from game_const import GRAVITY, SIZE, FPS, VEL_Y, VEL_X

class Player(Sprite):
  def __init__(self, width: int, height: int, color: Tuple[int, int, int]):
    super(Player, self).__init__()
    self.surf = Surface((width, height))
    self.surf.fill(color)
    self.vel_y = 0
    self.rect = self.surf.get_rect()
    self.rect.bottom = SIZE[1]/2

  def move_x(self, right):
    self.rect.move_ip(VEL_X if right else -VEL_X, 0)

    if 0 > self.rect.left: self.rect.left = 0
    if SIZE[0] < self.rect.right: self.rect.right = SIZE[0]

  def jump(self):    
    if self.vel_y == 0:
      self.vel_y = VEL_Y

  def apply_gravity(self):
    self.rect.move_ip(0, -self.vel_y)
    self.vel_y -= GRAVITY / FPS

    if self.rect.bottom > SIZE[1]: 
      self.rect.bottom = SIZE[1]
      self.vel_y = 0
  
  #def get_rect(self)

  def update(self, pressed_keys):
    self.apply_gravity()
    if pressed_keys[K_LEFT] or pressed_keys[K_a]:
      self.move_x(False)
    if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
      self.move_x(True)
    if pressed_keys[K_UP] or pressed_keys[K_w]:
      self.jump()