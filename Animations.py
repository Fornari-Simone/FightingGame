# region Imports
from enum import Enum
from game_const import Color
from pygame.image import load
from pygame.constants import RLEACCEL


# endregion Imports


class AnimationStates(Enum):
    IDLE = 0
    MOVE = 1
    JUMPUP = 3
    JUMPDOWN = 4
    ATTACK = 5


class Animation:
    def __init__(self, folder, numFrame) -> None:
        self.frames = []

        for i in range(numFrame):
            s = load(f"{folder}/{i}.png").convert()
            s.set_colorkey(Color.WHITE, RLEACCEL)
            self.frames.append(s)

        self.index = 0
        self.len = len(self.frames)

    def next(self):
        r = self.frames[self.index]
        self.index += 1
        if self.index == self.len:
            self.index = 0
        return r


# def reset(self): self.index = 0
