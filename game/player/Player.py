# region Imports

from game.player.Animations import Animation, AnimationStates as AS
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_z  # , K_x
from pygame.sprite import Group, Sprite, collide_rect
from game.const import Physics, Game, Color
from game.player.HealthBar import HealthBar
from pygame.surface import Surface
from pygame.transform import flip
from typing import Sequence

# endregion


class Player(Sprite):
    # region DocString
    """
    Represents a player of a fighting game. Should be extended to create a character
    """
    # endregion

    def __init__(
        self,
        facing: bool,
        nick: str,
        health: int,
        animationFrames: dict[AS, Animation],
        sprite_list: Group,
    ) -> None:
        # region Docstring
        """
        Creates a `Player` object

        ### Arguments
            `facing {bool}`:
                `summary`: boolean to display the player in the right direction
            `nick {str}`:
                `summary`: the username of the player
            `health {int}`:
                `summary`: the max health of the player
            `animationFrames {{AnimationState, Animation}}`:
                `summary`: a dictionary that associates every `AnimationState` with a `Animation` object
            `sprite_list {Group}`:
                `summary`: the sprite group in which to append internally generated sprites
        """
        # endregion

        super().__init__()

        # region Animation variables

        self.anims = animationFrames
        self.state = AS.IDLE
        self.current_anim_frame = 0
        self.animation_frames = 6
        self.current_atk_frame = 0
        self.atk_frames = 24
        self.chargedAtk = 0
        self.atk_cooldown_frames = 40
        self.cooldown = False

        # endregion

        # region Sprite variables

        self.image = self.anims[self.state].next()
        self.rect = self.image.get_rect()
        self.rect.bottom = Game.SIZE[1]

        self.facing = facing
        if not self.facing:
            self.image = flip(self.image, True, False)
            self.rect.right = Game.SIZE[0]

        # endregion

        self.vel_y = 0

        self.health = HealthBar(health, facing, nick)

        self.sprite_list = sprite_list

    def move_x(self, right: bool) -> None:
        # region DocString
        """
        Method to move the player in the given direction. The speed is defined in 'game_const.py'

        ### Arguments
            `right {bool}`:
                `summary`: true to move to the right, false to move to the left
        """
        # endregion

        # region Move the player

        self.facing = right
        self.rect.move_ip(Physics.VEL_X if right else -Physics.VEL_X, 0)

        # endregion

        # region Check if at the edge

        if 0 > self.rect.left:
            self.rect.left = 0
        if Game.SIZE[0] < self.rect.right:
            self.rect.right = Game.SIZE[0]

        # endregion

    def jump(self) -> None:
        # region DocString
        """
        Method to make the player jump. The upwards speed is defined in 'game_const.py'
        """
        # endregion

        if self.vel_y == 0:
            self.vel_y = Physics.VEL_Y

    def apply_gravity(self) -> None:
        # region DocString
        """
        Method to make the player affected by gravity. The gravity pull force is defined in 'game_const.py'
        """
        # endregion

        # region Move vertically

        self.rect.move_ip(0, -self.vel_y)
        self.vel_y -= Physics.GRAVITY / Game.FPS

        # endregion

        # region Check if at the bottom

        if self.rect.bottom >= Game.SIZE[1]:
            self.rect.bottom = Game.SIZE[1]
            self.vel_y = 0

        # endregion

    def standard_attack(self) -> None:
        # region DocString
        """
        Method to make the player do a normal attack
        """
        # endregion
        pass

    # @abstractmethod
    # def charged_attack(self) -> None:
    #     """
    #     Method to make the player do a charged attack
    #     """
    #     pass

    def checkDmg(self) -> bool:
        # region DocString
        """
        Method to check if the pleyer has been hit

        ### Returns
            `bool`: true if the player is dead, false otherwise
        """
        # endregion

        # region Check collision with attacks

        for atk in filter(
            lambda x: x.parent is not self,
            filter(lambda x: isinstance(x, Attack), self.sprite_list.sprites()),
        ):
            atk: Attack
            if collide_rect(self, atk):
                self.health.damage(atk.damage)
                atk.kill()
                return self.health.playerHealth == 0

        # endregion

    def animate(self, pressed_keys: Sequence) -> None:
        # region DocString
        """
        Method to animate the player

        ### Arguments
            `pressed_keys {Sequence}`:
                `summary`: a dictionary with the status of all keys
        """
        # endregion

        # region Set correct animation state

        if self.state is not AS.ATTACK:
            self.setState(AS.IDLE)
            if self.vel_y < 0:
                self.setState(AS.JUMPDOWN)
            elif self.vel_y > 0:
                self.setState(AS.JUMPUP)
            else:
                if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:
                    self.setState(AS.MOVE)

        # endregion

        # region Execute animation

        if self.current_anim_frame == self.animation_frames:
            self.current_anim_frame = 0
            self.image = (
                self.anims[self.state].next()
                if self.facing
                else flip(self.anims[self.state].next(), True, False)
            )
        self.current_anim_frame += 1

        # endregion

    def setState(self, state: AS) -> None:
        # region DocString
        """
        Method to set the animation state of the player
        """
        # endregion

        self.state = state

    def update(self, pressed_keys: Sequence) -> bool:
        # region DocString
        """
        Method to update the player every frame. Overridden from `Sprite`

        ### Arguments
            `pressed_keys {Sequence}`:
                `summary`: a dictionary with the status of all keys

        ### Returns
            `bool`: true if the player is dead, false otherwise
        """
        # endregion

        self.apply_gravity()

        # region Handle pressed keys

        if self.state not in [AS.ATTACK]:
            if pressed_keys[K_LEFT]:
                self.move_x(False)
            elif pressed_keys[K_RIGHT]:
                self.move_x(True)

            if pressed_keys[K_UP]:
                self.jump()

            if not self.cooldown:
                if pressed_keys[K_z]:
                    self.standard_attack()
                # if pressed_keys[K_x]:
                #     self.charged_attack()

        # endregion

        # region Attack cooldown

        if self.state in [AS.ATTACK] or self.cooldown:
            self.current_atk_frame += 1
            if self.current_atk_frame == self.atk_frames:
                self.setState(AS.IDLE)
                self.cooldown = True
            if self.current_atk_frame == (self.atk_frames + self.atk_cooldown_frames):
                self.cooldown = False
                self.current_atk_frame = 0

        # endregion

        self.animate(pressed_keys)

        return self.checkDmg()

    def draw(self, screen: Surface) -> None:
        # region DocString
        """
        Method to draw the player on the screen

        ### Arguments
            `screen {Surface}`:
                `summary`: the screen to draw in
        """
        # endregion

        screen.blit(self.image, self.rect)


class Ichigo(Player):
    # region DocString
    """
    Represents the selectable character Ichigo. Extended from `Player`
    """
    # endregion

    # region Constants

    IDLE = "img/Ichigo/Idle"
    MOVE = "img/Ichigo/Movement"
    JUMPUP = "img/Ichigo/JumpUp"
    JUMPDOWN = "img/Ichigo/JumpDown"
    ATTACK = "img/Ichigo/Attack"

    # endregion

    def __init__(self, facing: bool, nick: str, sprite_list: Group) -> None:
        # region DocString
        """
        Creates a `Ichigo` object

        ### Arguments
            `facing {bool}`:
                `summary`: boolean to display the player in the right direction
            `nick {str}`:
                `summary`: the username of the player
            `sprite_list {Group}`:
                `summary`: the sprite group in which to append internally generated sprites
        """
        # endregion

        # region Super constructor

        super(Ichigo, self).__init__(
            facing,
            nick,
            100,
            {
                AS.IDLE: Animation(Ichigo.IDLE, 4),
                AS.MOVE: Animation(Ichigo.MOVE, 8),
                AS.JUMPUP: Animation(Ichigo.JUMPUP, 2),
                AS.JUMPDOWN: Animation(Ichigo.JUMPDOWN, 2),
                AS.ATTACK: Animation(Ichigo.ATTACK, 4),
            },
            sprite_list,
        )

        # endregion

    def standard_attack(self):
        # region DocString
        """
        Method to make the player do a normal attack. Overridden from `Player`
        """
        # endregion

        # region Create a MeleeAttack if not in cooldown

        if self.current_atk_frame == 0:
            self.setState(AS.ATTACK)
            self.current_atk_frame = 0
            self.sprite_list.add(
                MeleeAttack(self, 0, 40, 50, 120, self.facing, 10, self.atk_frames)
            )

        # endregion

    # def charged_attack(self):
    #     pass


class Vegeth(Player):
    # region DocString
    """
    Represents the selectable character Vegeth. Extended from `Player`
    """
    # endregion

    # region Constants

    IDLE = "img/Vegeth/Idle"
    MOVE = "img/Vegeth/Movement"
    JUMPUP = "img/Vegeth/JumpUp"
    JUMPDOWN = "img/Vegeth/JumpDown"
    ATTACK = "img/Vegeth/Attack"

    # endregion

    def __init__(self, facing: bool, nick: str, sprite_list: Group) -> None:
        # region DocString
        """
        Creates a `Vegeth` object

        ### Arguments
            `facing {bool}`:
                `summary`: boolean to display the player in the right direction
            `nick {str}`:
                `summary`: the username of the player
            `sprite_list {Group}`:
                `summary`: the sprite group in which to append internally generated sprites
        """
        # endregion

        # region Super Constructor

        super(Vegeth, self).__init__(
            facing,
            nick,
            100,
            {
                AS.IDLE: Animation(Vegeth.IDLE, 4),
                AS.MOVE: Animation(Vegeth.MOVE, 4),
                AS.JUMPUP: Animation(Vegeth.JUMPUP, 1),
                AS.JUMPDOWN: Animation(Vegeth.JUMPDOWN, 1),
                AS.ATTACK: Animation(Vegeth.ATTACK, 5),
            },
            sprite_list,
        )

        # endregion

        self.atk_frames = 30

    def standard_attack(self):
        # region DocString
        """
        Method to make the player do a normal attack. Overridden from `Player`
        """
        # endregion

        # region Create a MeleeAttack if not in cooldown

        if self.current_atk_frame == 0:
            self.setState(AS.ATTACK)
            self.current_atk_frame = 0
            self.sprite_list.add(
                MeleeAttack(self, 0, 70, 40, 50, self.facing, 10, self.atk_frames)
            )

        # endregion

    # def charged_attack(self):
    #     pass


class Attack(Sprite):
    # region DocString
    """
    Represents an generic attack of a player.
    """
    # endregion

    def __init__(
        self,
        parent: Player,
        speed: int,
        x: int,
        y: int,
        width: int,
        height: int,
        color: tuple[int, int, int],
        facing: bool,
        damage: int,
        lifespan: int,
    ) -> None:
        # region DocString
        """
        Creates a `Attack` object

        ### Arguments
            `parent {Player}`:
                `summary`: the player who attacked
            `speed {int}`:
                `summary`: the speed at which the attacks move
            `x {int}`:
                `summary`: the x coordinate relative to the player
            `y {int}`:
                `summary`: the y coordinate relative to the player
            `width {int}`:
                `summary`: the width of the attack hitbox
            `height {int}`:
                `summary`: the height of the attack hitbox
            `color {(int, int, int)}`:
                `summary`: the color of the attack sprite
            `facing {bool}`:
                `summary`: true if the player is facing to the right, false otherwise
            `damage {int}`:
                `summary`: the damage dealt by the attack
            `lifespan {int}`:
                `summary`: for how much the attack can exist without hitting another player
        """
        # endregion

        super(Attack, self).__init__()

        # region Sprite variables

        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(
            parent.rect.right if facing else (parent.rect.x - width), parent.rect.y
        )
        self.rect.move_ip(x, y)

        # endregion

        self.parent = parent
        self.speed = speed
        self.damage = damage
        self.lifespan = lifespan
        self.current_life_frame = 0

    def update(self, pressed_keys: Sequence) -> None:
        # region DocString
        """
        Method called every frame to update the object

        ### Arguments
            `pressed_keys {Sequence}`:
                `summary`: a dictionary with the status of all keys
        """
        # endregion

        # region Destroy if expired

        if self.current_life_frame == self.lifespan:
            self.kill()
        self.current_life_frame += 1

        # endregion

        self.rect.move_ip(self.speed, 0)


class MeleeAttack(Attack):
    # region DocString
    """
    Represents a melee attack. Extended from `Attack`.\n
    The attack spawns directly in front of the player and it's transparent
    """
    # endregion

    def __init__(
        self,
        parent: Player,
        x: int,
        y: int,
        width: int,
        height: int,
        facing: bool,
        damage: int,
        lifespan: int,
    ) -> None:
        # region DocString
        """
        Creates a `Attack` object

        ### Arguments
            `parent {Player}`:
                `summary`: the player who attacked
            `x {int}`:
                `summary`: the x coordinate relative to the player
            `y {int}`:
                `summary`: the y coordinate relative to the player
            `width {int}`:
                `summary`: the width of the attack hitbox
            `height {int}`:
                `summary`: the height of the attack hitbox
            `facing {bool}`:
                `summary`: true if the player is facing to the right, false otherwise
            `damage {int}`:
                `summary`: the damage dealt by the attack
            `lifespan {int}`:
                `summary`: for how much the attack can exist without hitting another player
        """
        # endregion

        super(MeleeAttack, self).__init__(
            parent, 0, x, y, width, height, Color.RED, facing, damage, lifespan
        )

        self.image.set_colorkey(Color.RED)


class RangedAttack(Attack):
    # region DocString
    """
    Represents a ranged attack. Extended from `Attack`.\n
    Spawns a green projectile that travels across the map and die apon reaching the borders
    """
    # endregion

    def __init__(
        self,
        parent: Player,
        speed: int,
        x: int,
        y: int,
        width: int,
        height: int,
        facing: bool,
        damage: int,
        lifespan: int,
    ) -> None:
        # region DocString
        """
        Creates a `Attack` object

        ### Arguments
            `parent {Player}`:
                `summary`: the player who attacked
            `speed {int}`:
                `summary`: the speed at which the attacks move
            `x {int}`:
                `summary`: the x coordinate relative to the player
            `y {int}`:
                `summary`: the y coordinate relative to the player
            `width {int}`:
                `summary`: the width of the attack hitbox
            `height {int}`:
                `summary`: the height of the attack hitbox
            `facing {bool}`:
                `summary`: true if the player is facing to the right, false otherwise
            `damage {int}`:
                `summary`: the damage dealt by the attack
            `lifespan {int}`:
                `summary`: for how much the attack can exist without hitting another player
        """
        # endregion

        super(RangedAttack, self).__init__(
            parent, speed, x, y, width, height, Color.GREEN, facing, damage, lifespan
        )

    def update(self, pressed_keys: Sequence) -> None:
        # region DocString
        """
        Method called every frame to update the object

        ### Arguments
            `pressed_keys {Sequence}`:
                `summary`: a dictionary with the status of all keys
        """
        # endregion

        super(RangedAttack, self).update(pressed_keys)

        if 0 > self.rect.left or Game.SIZE[0] < self.rect.right:
            self.kill()
