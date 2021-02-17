# region Imports

from enum import Enum
from pygame.image import load
from pygame.transform import scale2x

# endregion Imports


class AnimationStates(Enum):
    IDLE = 0
    MOVE = 1
    JUMPUP = 2
    JUMPDOWN = 3
    ATTACK = 4
    COOLDOWN = -1


class Animation:
    def __init__(self, folder, numFrame) -> None:
        self.frames = []

        for i in range(numFrame):
            s = load(f"{folder}/{i}.png").convert_alpha()
            s = scale2x(s)
            self.frames.append(s)

        self.index = 0
        self.len = len(self.frames)

    def next(self):
        r = self.frames[self.index]
        self.index += 1
        if self.index == self.len:
            self.index = 0
        return r
