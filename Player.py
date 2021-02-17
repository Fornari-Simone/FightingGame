# region Imports
from HealthBar import HealthBar
from Attack import Attack, MeleeAttack
from pygame.locals import K_LEFT, K_a, K_RIGHT, K_d, K_UP, K_w, K_z, K_x
from game_const import Physics, Game
from pygame.sprite import Sprite, collide_rect
from pygame.transform import flip
from Animations import Animation, AnimationStates as AS
from pygame.time import get_ticks

# endregion


class Player(Sprite):
    def __init__(
        self,
        facing,
        health,
        animationFrames,
        sprite_list,
    ):
        super().__init__()
        self.anims = animationFrames
        self.image = self.anims[AS.IDLE].next()
        self.rect = self.image.get_rect()
        self.rect.bottom = Game.SIZE[1]

        self.facing = facing
        if not self.facing:
            self.image = flip(self.image, True, False)
            self.rect.right = Game.SIZE[0]

        self.state = AS.IDLE
        self.current_anim_frame = 0
        self.animation_frames = 6

        self.vel_y = 0

        self.current_atk_frame = 0
        self.atk_frames = 24
        self.chargedAtk = 0
        self.atk_cooldown_frames = 40
        self.cooldown = False

        self.health = HealthBar(health, facing)

        self.sprite_list = sprite_list

    def move_x(self, right):
        self.facing = right
        self.rect.move_ip(Physics.VEL_X if right else -Physics.VEL_X, 0)

        if 0 > self.rect.left:
            self.rect.left = 0
        if Game.SIZE[0] < self.rect.right:
            self.rect.right = Game.SIZE[0]

    def jump(self):
        if self.vel_y == 0:
            self.vel_y = Physics.VEL_Y

    def apply_gravity(self):
        self.rect.move_ip(0, -self.vel_y)
        self.vel_y -= Physics.GRAVITY / Game.FPS

        if self.rect.bottom >= Game.SIZE[1]:
            self.rect.bottom = Game.SIZE[1]
            self.vel_y = 0

    def melee_attack(self):
        # if get_ticks() >= self.lastAtk + 500:
        #     self.lastAtk = get_ticks()
        #     self.sprite_list.add(MeleeAttack(self, 30, 45, self.facing, 10))
        pass

    def charged_attack(self):
        # if get_ticks() >= self.lastAtk + 500:
        #     self.lastAtk = get_ticks()
        #     self.sprite_list.add(
        #         RangedAttack(self, 20 if self.facing else -20, 10, 10, self.facing, 10)
        #     )
        pass

    def checkDmg(self):
        atks = list(
            filter(
                lambda x: x.parent is not self,
                filter(lambda x: isinstance(x, Attack), self.sprite_list.sprites()),
            )
        )

        for atk in atks:
            if collide_rect(self, atk):
                self.health.damage(atk.damage)
                atk.kill()

    def animate(self, pressed_keys):
        if self.state is not AS.ATTACK:
            self.setState(AS.IDLE)
            if self.vel_y < 0:
                self.setState(AS.JUMPDOWN)
            elif self.vel_y > 0:
                self.setState(AS.JUMPUP)
            else:
                if (
                    pressed_keys[K_a]
                    or pressed_keys[K_LEFT]
                    or pressed_keys[K_d]
                    or pressed_keys[K_RIGHT]
                ):
                    self.setState(AS.MOVE)

        if self.current_anim_frame == self.animation_frames:
            self.current_anim_frame = 0
            self.image = (
                self.anims[self.state].next()
                if self.facing
                else flip(self.anims[self.state].next(), True, False)
            )
        self.current_anim_frame += 1

    def setState(self, state):
        self.state = state

    def update(self, pressed_keys):
        self.apply_gravity()

        self.checkDmg()

        self.animate(pressed_keys)

        if self.state not in [AS.ATTACK]:
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.move_x(False)
            elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.move_x(True)

            if pressed_keys[K_UP] or pressed_keys[K_w]:
                self.jump()

            if not self.cooldown:
                if pressed_keys[K_z]:
                    self.melee_attack()
                if pressed_keys[K_x]:
                    self.charged_attack()

        if self.state in [AS.ATTACK] or self.cooldown:
            self.current_atk_frame += 1
            if self.current_atk_frame == self.atk_frames:
                self.setState(AS.IDLE)
                self.cooldown = True
            if self.current_atk_frame == (self.atk_frames + self.atk_cooldown_frames):
                self.cooldown = False
                self.current_atk_frame = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Ichigo(Player):
    def __init__(self, facing, sprite_list):
        super().__init__(
            facing,
            100,
            {
                AS.IDLE: Animation("img/Ichigo/Idle", 4),
                AS.MOVE: Animation("img/Ichigo/Movement", 8),
                AS.JUMPUP: Animation("img/Ichigo/JumpUp", 2),
                AS.JUMPDOWN: Animation("img/Ichigo/JumpDown", 2),
                AS.ATTACK: Animation("img/Ichigo/Attack", 4),
            },
            sprite_list,
        )

    def melee_attack(self):
        if self.current_atk_frame == 0:
            self.setState(AS.ATTACK)
            self.current_atk_frame = 0
            self.sprite_list.add(
                MeleeAttack(self, 0, 40, 50, 120, self.facing, 10, self.atk_frames)
            )

    def charged_attack(self):
        pass


class Vegeth(Player):
    def __init__(self, facing, sprite_list):
        super().__init__(
            facing,
            100,
            {
                AS.IDLE: Animation("img/Vegeth/Idle", 4),
                AS.MOVE: Animation("img/Vegeth/Movement", 4),
                AS.JUMPUP: Animation("img/Vegeth/JumpUp", 1),
                AS.JUMPDOWN: Animation("img/Vegeth/JumpDown", 1),
                AS.ATTACK: Animation("img/Vegeth/Attack", 4),
            },
            sprite_list,
        )
        self.atk_frames = 30

    def melee_attack(self):
        if self.current_atk_frame == 0:
            self.setState(AS.ATTACK)
            self.current_atk_frame = 0
            self.sprite_list.add(
                MeleeAttack(self, 0, 70, 40, 50, self.facing, 10, self.atk_frames)
            )
        self.current_frame += 1
    def charged_attack(self):
        pass