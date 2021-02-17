# region Imports
from pygame.time import get_ticks
from game_const import Color, Game
from pygame.sprite import Sprite
from pygame import Surface
from typing import Tuple

# endregion Imports


class Attack(Sprite):
    def __init__(
        self,
        parent,
        speed: int,
        width: int,
        height: int,
        color: Tuple[int, int, int],
        facing: bool,
        damage: int,
    ):
        super().__init__()
        self.surf = Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.move_ip(
            parent.rect.right if facing else (parent.rect.x - width), parent.rect.y
        )
        self.parent = parent
        self.speed = speed
        self.damage = damage

    def update(self, pressed_keys):
        pass


class MeleeAttack(Attack):
    def __init__(
        self, parent, width: int, height: int, facing: bool, damage: int
    ):
        super().__init__(parent, 0, width, height, Color.RED, facing, damage)
        self.timer = get_ticks()

    def update(self, _):
        if get_ticks() >= self.timer + 250:
            self.kill()


class RangedAttack(Attack):
    def __init__(
        self,
        parent,
        speed: int,
        width: int,
        height: int,
        facing: bool,
        damage: int,
    ):
        super().__init__(parent, speed, width, height, Color.GREEN, facing, damage)

    def update(self, _):
        self.rect.move_ip(self.speed, 0)

        if 0 > self.rect.left or Game.SIZE[0] < self.rect.right:
            self.kill()
