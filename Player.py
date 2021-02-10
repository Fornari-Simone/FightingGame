	# region Imports

	from pygame.constants import K_z
	from pygame.locals import K_LEFT, K_a, K_RIGHT, K_d, K_UP, K_w
	from pygame.time import get_ticks
	from game_const import GRAVITY, SIZE, FPS, VEL_Y, VEL_X
	from pygame.sprite import Group, Sprite
	from pygame import Surface
	from typing import Tuple

	# endregion


	class Player(Sprite):
		def __init__(
				self,
				width: int,
				height: int,
				color: Tuple[int, int, int],
				life: int,
				sprite_list,
		):
				super().__init__()
				self.surf = Surface((width, height))
				self.surf.fill(color)
				self.vel_y = 0
				self.rect = self.surf.get_rect()
				self.rect.bottom = SIZE[1] / 2
				self.sprite_list = sprite_list
				self.lastAtk = 0
				self.facing = True
				self.life = life

		def move_x(self, right):
				self.facing = right
				self.rect.move_ip(VEL_X if right else -VEL_X, 0)

				if 0 > self.rect.left:
						self.rect.left = 0
				if SIZE[0] < self.rect.right:
						self.rect.right = SIZE[0]

		def jump(self):
				if self.vel_y == 0:
						self.vel_y = VEL_Y

		def apply_gravity(self):
				self.rect.move_ip(0, -self.vel_y)
				self.vel_y -= GRAVITY / FPS

				if self.rect.bottom > SIZE[1]:
						self.rect.bottom = SIZE[1]
						self.vel_y = 0

		def attack(self):
				if get_ticks() >= self.lastAtk + 500:
						self.lastAtk = get_ticks()
						self.sprite_list.add(MeleeAttack(self, 30, 45, self.facing, 10))
						self.sprite_list.add(
								RangedAttack(self, 20 if self.facing else -20, 10, 10, self.facing, 10)
						)
						
		def checkDmg(self):
				atks = list(filter(lambda x: x.parent is not self, filter(lambda x: isinstance(x, Attack), self.sprite_list.sprites())))
				print(atks)
				print(atks[0].parent.color)
				
				for atk in atks:
					atk.parent.life -= atk.damage
					print(atk.parent.life)

		def update(self, pressed_keys):
				self.apply_gravity()
				if pressed_keys[K_LEFT] or pressed_keys[K_a]:
						self.move_x(False)
				if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
						self.move_x(True)
				if pressed_keys[K_UP] or pressed_keys[K_w]:
						self.jump()
				if pressed_keys[K_z]:
						self.attack()
				self.checkDmg()


	class Attack(Sprite):
		def __init__(
				self,
				parent: Player,
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
				self, parent: Player, width: int, height: int, facing: bool, damage: int
		):
				super().__init__(parent, 0, width, height, (255, 0, 0), facing, damage)
				self.timer = get_ticks()

		def update(self, _):
			if get_ticks() >= self.timer + 250:
				self.kill()


	class RangedAttack(Attack):
		def __init__(
				self,
				parent: Player,
				speed: int,
				width: int,
				height: int,
				facing: bool,
				damage: int,
		):
				super().__init__(parent, speed, width, height, (0, 255, 0), facing, damage)

		def update(self, _):
				self.rect.move_ip(self.speed, 0)

				if 0 > self.rect.left or SIZE[0] < self.rect.right:
						self.kill()