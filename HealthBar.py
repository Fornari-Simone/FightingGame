# region Imports
from game_const import Game
from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import flip, scale

# endregion Imports


class HealthBar(Sprite):
    def __init__(self, maxHealth: int, facing: bool):
        super().__init__()
        self.gaugeImg = load("img/HealthBar/gauge.png").convert_alpha()
        self.gaugeRect = self.gaugeImg.get_rect()
        self.gaugeRect.move_ip(
            10 if facing else Game.SIZE[0] - self.gaugeRect.width - 10, 10
        )
        self.lifeImg = load("img/HealthBar/life.png").convert_alpha()
        self.lifeRect = self.lifeImg.get_rect()
        self.lifeRect.move_ip(
            10 if facing else Game.SIZE[0] - self.lifeRect.width - 10, 10
        )

        if not facing:
            self.gaugeImg = flip(self.gaugeImg, True, False)
            self.lifeImg = flip(self.lifeImg, True, False)

        self.facing = facing

        self.playerHealth = maxHealth
        self.maxHealth = maxHealth

    def damage(self, dmg):
        self.playerHealth -= dmg
        self.lifeImg = scale(
            self.lifeImg,
            (
                int((self.playerHealth / self.maxHealth) * self.lifeRect.width),
                self.lifeRect.height,
            ),
        )
        if not self.facing:
            self.lifeRect.move_ip(int(self.playerHealth / self.maxHealth), 0)

    def draw(self, screen):
        screen.blits(((self.lifeImg, self.lifeRect), (self.gaugeImg, self.gaugeRect)))
