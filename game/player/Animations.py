# region Imports

from pygame.transform import scale2x
from pygame.surface import Surface
from pygame.image import load
from enum import Enum

# endregion Imports


class AnimationStates(Enum):
    # region DocString
    """
    The state in which an `Animation` can be
    """
    # endregion

    IDLE = 0
    MOVE = 1
    JUMPUP = 2
    JUMPDOWN = 3
    ATTACK = 4
    COOLDOWN = -1


class Animation:
    # region DocString
    """
    Represents a sprite animation. The frames must all be in a single folder as PNG files\n
    named in order with only numbers starting from 0
    """
    # endregion

    def __init__(self, folder: str, numFrame: int) -> None:
        # region DocString
        """
        Creates a `Animation` object

        ### Arguments
            `folder {str}`:
                `summary`: the folder containing the frames
            `numFrame {int}`:
                `summary`: number of frames in the animation
        """
        # endregion

        self.frames = []

        # region Load frames

        for i in range(numFrame):
            s = load(f"{folder}/{i}.png").convert_alpha()
            s = scale2x(s)
            self.frames.append(s)

        # endregion

        self.index = 0
        self.len = len(self.frames)

    def next(self) -> Surface:
        # region DocString
        """
        A method to get the next frame of the animation. This method cycles trough the list of frames,\n
        resetting every time the end is reached
        """
        # endregion

        r = self.frames[self.index]
        self.index += 1
        if self.index == self.len:
            self.index = 0
        return r
