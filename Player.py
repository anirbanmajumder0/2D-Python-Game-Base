import pygame
from spritesheetparser import Spritesheet

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
		self.UP_KEY, self.DOWN_KEY, self.FACING_DOWN = False, False, False
		self.is_jumping, self.on_ground = False, False
		self.gravity, self.friction = .35, -.09
		self.image = Spritesheet('resources/Blockz').get_sprite('white.png')
		self.image = pygame.transform.scale(self.image, (32,32))
		self.rect = self.image.get_rect()
		self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
		self.acceleration = pygame.math.Vector2(5,5)
		self.left_border = 0
		self.top_border = 0
		self.bottom_border = 1280
		self.right_border = 2400
		self.max_vel = 8

	def draw(self, display,camera_offset_x,camera_offset_y):
		display.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y - camera_offset_y))


	def update(self, dt, tiles):
		self.vertical_movement(dt)
		self.horizontal_movement(dt)
		#print(self.rect)
		#print(self.rect.w)
	
		self.checkCollisionsy(tiles)
		self.checkCollisionsx(tiles)


	def horizontal_movement(self,dt):		
		self.acceleration.x = 0
		if self.LEFT_KEY:
			self.acceleration.x -= .6
		elif self.RIGHT_KEY:
			self.acceleration.x += .6
		self.acceleration.x += self.velocity.x * self.friction
		self.velocity.x += self.acceleration.x * dt
		self.limit_x_velocity(self.max_vel)
		self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
		self.rect.x = self.position.x


	def vertical_movement(self,dt):
		self.acceleration.y = 0
		if self.UP_KEY:
			self.acceleration.y -= .6
		elif self.DOWN_KEY:
			self.acceleration.y += .6
		self.acceleration.y += self.velocity.y * self.friction
		self.velocity.y += self.acceleration.y * dt
		self.limit_y_velocity(self.max_vel)
		self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
		self.rect.y = self.position.y


	def limit_x_velocity(self, max_vel):
		self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
		if abs(self.velocity.x) < .11: self.velocity.x = 0


	def limit_y_velocity(self, max_vel):
		self.velocity.y = max(-max_vel, min(self.velocity.y, max_vel))
		if abs(self.velocity.y) < .11: self.velocity.y = 0


	def get_hits(self, tiles):
		hits = []
		for tile in tiles:
			if self.rect.colliderect(tile):
				if tile.can_collide :
					hits.append(tile)
					#print(tile.rect)
		return hits


	def checkCollisionsx(self, tiles):
		collisions = self.get_hits(tiles)
		for tile in collisions:
			if self.velocity.x > 0:  # Hit tile moving right
				self.position.x = tile.rect.left - self.rect.w
				self.rect.x = self.position.x
				self.velocity.x = 0
			elif self.velocity.x < 0:  # Hit tile moving left
				self.position.x = tile.rect.right
				self.rect.x = self.position.x
				self.velocity.x = 0
			

	def checkCollisionsy(self, tiles):
		collisions = self.get_hits(tiles)
		for tile in collisions:
			if self.velocity.y > 0:  # Hit tile moving down
				self.position.y = tile.rect.top - self.rect.h
				self.rect.y = self.position.y
				self.velocity.y = 0
			elif self.velocity.y < 0:  # Hit tile moving up
				self.position.y = tile.rect.bottom
				self.rect.y = self.position.y
				self.velocity.y = 0
		