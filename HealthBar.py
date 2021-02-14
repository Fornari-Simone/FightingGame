# region Imports
from pygame.sprite import Sprite
from pygame.transform import scale
from pygame import Surface
from Player import Player

# endregion Imports


class HealthBar(Sprite):
    def __init__(self, player: Player, maxHealth: int, x, y):
        super().__init__()
        self.surfBg = Surface((100, 20))
        self.rectBg = self.surfBg.get_rect()
        self.surfBg.fill((10, 10, 10))
        self.surfBar = Surface((100, 20))
        self.surfBar.fill((255, 0, 0))
        self.rectBar = self.surfBar.get_rect()
        self.rectBg.move_ip(x, y)
        self.rectBar.move_ip(x, y)

        self.player = player
        self.maxHealth = maxHealth

    def update(self, pressed_keys):
        # self.rectBar.width = (self.player.health / self.maxHealth) * 100
        self.surfBar = scale(
            self.surfBar, (int((self.player.health / self.maxHealth) * 100), 20)
        )
