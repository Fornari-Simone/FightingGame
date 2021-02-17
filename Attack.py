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
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int],
        facing: bool,
        damage: int,
        lifespan: int,
    ):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(
            parent.rect.right if facing else (parent.rect.x - width), parent.rect.y
        )
        self.rect.move_ip(x, y)

        self.parent = parent
        self.speed = speed
        self.damage = damage
        self.lifespan = lifespan
        self.current_life_frame = 0

    def update(self, pressed_keys):
        if self.current_life_frame == self.lifespan:
            self.kill()
        self.current_life_frame += 1

        self.rect.move_ip(self.speed, 0)


class MeleeAttack(Attack):
    def __init__(
        self,
        parent,
        x: int,
        y: int,
        width: int,
        height: int,
        facing: bool,
        damage: int,
        lifespan: int,
    ):
        super().__init__(
            parent, 0, x, y, width, height, Color.RED, facing, damage, lifespan
        )
        self.timer = get_ticks()


class RangedAttack(Attack):
    def __init__(
        self,
        parent,
        speed: int,
        x: int,
        y: int,
        width: int,
        height: int,
        facing: bool,
        damage: int,
        lifespan: int,
    ):
        super().__init__(
            parent, speed, x, y, width, height, Color.GREEN, facing, damage, lifespan
        )

    def update(self, _):
        super().update(_)

        if 0 > self.rect.left or Game.SIZE[0] < self.rect.right:
            self.kill()
