# region Imports

from pygame.transform import flip, scale
from game.const import Color, Game
from pygame.sprite import Sprite
from pygame.font import SysFont
from pygame.image import load

# endregion Imports


class HealthBar(Sprite):
    # region DocString
    """
    Represents the health bar of a player and also displays its username
    """
    # endregion

    def __init__(self, maxHealth: int, isPlayer1: bool, nick: str) -> None:
        # region DocString
        """
        Creates a `HealthBar` object

        ### Arguments
            `maxHealth {int}`:
                `summary`: the starting health of the player
            `isPlayer1 {bool}`:
                `summary`: boolean to display the bar in the right direction
            `nick {str}`:
                `summary`: the username of the player
        """
        # endregion

        super().__init__()

        self.isPlayer1 = isPlayer1

        # region Gauge sprite

        self.gaugeImg = load(Game.GAUGE_PATH).convert_alpha()
        self.gaugeRect = self.gaugeImg.get_rect()
        self.gaugeRect.move_ip(
            10 if self.isPlayer1 else Game.SIZE[0] - self.gaugeRect.width - 10, 10
        )

        # endregion

        # region Bar sprite

        self.lifeImg = load(Game.LIFEBAR_PATH).convert_alpha()
        self.lifeRect = self.lifeImg.get_rect()
        self.lifeRect.move_ip(
            10 if self.isPlayer1 else Game.SIZE[0] - self.lifeRect.width - 10, 10
        )

        # endregion

        if not self.isPlayer1:
            self.gaugeImg = flip(self.gaugeImg, True, False)
            self.lifeImg = flip(self.lifeImg, True, False)

        self.nick = SysFont(Game.FONT, 30).render(nick.strip(), False, Color.WHITE)
        self.nickRect = self.nick.get_rect()
        self.nickRect.move_ip(
            15 if self.isPlayer1 else Game.SIZE[0] - self.nickRect.width - 15,
            self.gaugeRect.height + 15,
        )

        self.playerHealth = maxHealth
        self.maxHealth = maxHealth

    def damage(self, dmg: int) -> None:
        # region DocString
        """
        Method to deal damage to the player

        ### Arguments
            `dmg {int}`:
                `summary`: the damage to deal
        """
        # endregion

        # region Life can't go below 0

        self.playerHealth -= dmg
        if self.playerHealth < 0:
            self.playerHealth = 0

        # endregion

        # region Flip if pl2

        if not self.isPlayer1:
            self.lifeRect.move_ip(
                int((dmg / self.maxHealth) * self.lifeRect.width),
                0,
            )

        # endregion

        # region Decrese lifebar

        self.lifeImg = scale(
            self.lifeImg,
            (
                int((self.playerHealth / self.maxHealth) * self.lifeRect.width),
                self.lifeRect.height,
            ),
        )

        # endregion

    def draw(self, screen) -> None:
        # region DocString
        """
        Method to draw the health bar and the username on the screen

        ### Arguments
            `screen {Surface}`:
                `summary`: the screen to draw in
        """
        # endregion

        screen.blits(
            (
                (self.lifeImg, self.lifeRect),
                (self.gaugeImg, self.gaugeRect),
                (self.nick, self.nickRect),
            )
        )
