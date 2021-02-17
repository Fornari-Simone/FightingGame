# region Imports
from Attack import Attack
from pygame.constants import RLEACCEL
from pygame.locals import K_LEFT, K_a, K_RIGHT, K_d, K_UP, K_w, K_z, K_x
from game_const import Physics, Game
from pygame.sprite import Sprite, collide_rect
from pygame.transform import flip
from pygame.image import load
from Animations import AnimationStates, Animation

# endregion


class Player(Sprite):
    def __init__(
        self,
        # width: int,
        # height: int,
        # color: Tuple[int, int, int],
        health: int,
        sprite_list,
    ):
        super().__init__()
<<<<<<< HEAD
<<<<<<< HEAD
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

=======
=======
>>>>>>> parent of 30d4737 (Merge branch 'master' of https://github.com/Fornari-Simone/FightingGame)
        # self.surf = load("img/Ichigo/idle/1.png").convert()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # self.rect = self.surf.get_rect()
        # self.rect.bottom = Game.SIZE[1] / 2
        # self.surf = Surface((width, height))
        # self.surf.fill(color)

        self.state = AnimationStates.IDLE
        self.current_frame = 0
        self.animation_frame = 6

<<<<<<< HEAD
        self.vel_y = 0
>>>>>>> parent of c152f7f (add animation jump, movement,)
=======
        self.vel_y = -Physics.VEL_Y
>>>>>>> parent of 30d4737 (Merge branch 'master' of https://github.com/Fornari-Simone/FightingGame)
        self.sprite_list = sprite_list
        self.lastAtk = 0
        self.facing = True
        self.health = health
        # self.color = color

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

        if self.rect.bottom > Game.SIZE[1]:
            self.rect.bottom = Game.SIZE[1]
            self.vel_y = 0

    def melee_attack(self):
        # if get_ticks() >= self.lastAtk + 500:
        #     self.lastAtk = get_ticks()
        #     self.sprite_list.add(MeleeAttack(self, 30, 45, self.facing, 10))
        pass

    def ranged_attack(self):
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

        # self.surf.fill(self.color)
        for atk in atks:
            if collide_rect(self, atk):
                self.health -= atk.damage
                atk.kill()
                # self.surf.fill((255, 0, 255))

    def animate(self):
        pass

    def update(self, pressed_keys):
        self.apply_gravity()
<<<<<<< HEAD
<<<<<<< HEAD

=======
        if pressed_keys[K_LEFT]:
            self.move_x(False)
            self.state = AnimationStates.MOVE
        if pressed_keys[K_RIGHT]:
            self.move_x(True)
            self.state = AnimationStates.MOVE
        if pressed_keys[K_UP]:
            self.jump()
        if pressed_keys[K_z]:
            self.melee_attack()
        if pressed_keys[K_x]:
            self.ranged_attack()
        if not(self.rect.bottom == Game.SIZE[1]):
            if self.vel_y > 0: 
                self.state = AnimationStates.JUMPUP
            if self.vel_y < 0: 
                self.state = AnimationStates.JUMPDOWN
        elif not pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT] and not pressed_keys[K_UP] and not pressed_keys[K_z] and not pressed_keys[K_x]:
            self.state = AnimationStates.IDLE
>>>>>>> parent of 30d4737 (Merge branch 'master' of https://github.com/Fornari-Simone/FightingGame)
        self.checkDmg()
        self.animate()


class Ichigo(Player):
<<<<<<< HEAD
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
=======
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.move_x(False)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.move_x(True)
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.jump()
        if pressed_keys[K_z]:
            self.melee_attack()
        if pressed_keys[K_x]:
            self.ranged_attack()
        self.checkDmg()

        self.animate()


class Ichigo(Player):
    def __init__(self, health: int, sprite_list):
        super().__init__(health, sprite_list)
        self.image = load("img/Ichigo/idle/1.png").convert()
=======
    def __init__(self, health: int, sprite_list):
        super().__init__(health, sprite_list)
        self.image = load("img/Ichigo/Idle/1.png").convert()
>>>>>>> parent of 30d4737 (Merge branch 'master' of https://github.com/Fornari-Simone/FightingGame)
        self.rect = self.image.get_rect()
        self.rect.bottom = Game.SIZE[1] / 2
        self.anims = [
            Animation("img/Ichigo/Idle", 4),
            Animation("img/Ichigo/Movement", 8),
            Animation("img/Ichigo/JumpUp", 2),
            Animation("img/Ichigo/JumpDown", 2),
<<<<<<< HEAD
            # Animation("img/Ichigo/Attack", 4),
=======
            Animation("img/Ichigo/Attack", 4),
>>>>>>> parent of 30d4737 (Merge branch 'master' of https://github.com/Fornari-Simone/FightingGame)
        ]
    
    def move_x(self, right):
        super().move_x(right)
<<<<<<< HEAD
>>>>>>> parent of c152f7f (add animation jump, movement,)
=======
>>>>>>> parent of 30d4737 (Merge branch 'master' of https://github.com/Fornari-Simone/FightingGame)

    def melee_attack(self):
        pass

<<<<<<< HEAD
<<<<<<< HEAD

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
                AS.ATTACK: Animation("img/Vegeth/Attack", 5),
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
<<<<<<< HEAD
=======
=======
    def ranged_attack(self):
        pass

    def animate(self):
        if self.current_frame == self.animation_frame:
            self.current_frame = 0
            self.image = (
                self.anims[self.state.value].next()
                if self.facing
                else flip(self.anims[self.state.value].next(), True, False)
            )
        self.current_frame += 1
=======
>>>>>>> parent of f8655d0 (deleted)
        
class Vegeth(Player):
    def __init__(self, health: int, sprite_list):
        super().__init__(health, sprite_list)
        self.image = load("img/Vegeth/Idle/0.png").convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = Game.SIZE[1] / 2
        self.anims = [
            Animation("img/Vegeth/Idle", 4),
            Animation("img/Vegeth/Movement", 4),
            Animation("img/Vegeth/JumpUp", 2),
            Animation("img/Vegeth/JumpDown", 2),
            Animation("img/Vegeth/Attack", 4),
        ]
    
    def move_x(self, right):
        super().move_x(right)

    def melee_attack(self):
        pass

    def ranged_attack(self):
        pass

<<<<<<< HEAD
>>>>>>> parent of 30d4737 (Merge branch 'master' of https://github.com/Fornari-Simone/FightingGame)
=======
>>>>>>> parent of f8655d0 (deleted)
    def animate(self):
        if self.current_frame == self.animation_frame:
            self.current_frame = 0
            self.image = (
                self.anims[self.state.value].next()
                if self.facing
                else flip(self.anims[self.state.value].next(), True, False)
            )
<<<<<<< HEAD
<<<<<<< HEAD
        self.current_frame += 1
>>>>>>> parent of c152f7f (add animation jump, movement,)
=======
        self.current_frame += 1
>>>>>>> parent of 30d4737 (Merge branch 'master' of https://github.com/Fornari-Simone/FightingGame)
=======
        self.current_frame += 1
    def charged_attack(self):
        pass
>>>>>>> parent of f8655d0 (deleted)
