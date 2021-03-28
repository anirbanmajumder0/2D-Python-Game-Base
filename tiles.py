import pygame, csv, os

class Tile(pygame.sprite.Sprite):
	def __init__(self, image, x, y, spritesheet,can_collide):
		pygame.sprite.Sprite.__init__(self)
		self.image = spritesheet.get_sprite(image)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y
		self.can_collide = can_collide

	def draw(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
	def __init__(self, filename, spritesheet):
		self.tile_size = 32
		self.start_x, self.start_y = 0, 0
		self.spritesheet = spritesheet
		self.tiles = self.load_tiles(filename)
		self.map_surface = pygame.Surface((self.map_w, self.map_h))
		self.map_surface.set_colorkey((0, 0, 0))
		self.load_map()

	def draw_map(self, surface,xx,yy):
		surface.blit(self.map_surface, (0-xx, 0-yy))

	def load_map(self):
		for tile in self.tiles:
			tile.draw(self.map_surface)

	def read_csv(self, filename):
		map = []
		with open(os.path.join(filename)) as data:
			data = csv.reader(data, delimiter=',')
			for row in data:
				map.append(list(row))
		return map

	def load_tiles(self, filename):
		tiles = []
		map = self.read_csv(filename)
		x, y = 0, 0
		for row in map:
			x = 0
			for tile in row:
				if tile == '0':
					self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
				elif tile == '1':
					tiles.append(Tile('dirt2.png', x * self.tile_size, y * self.tile_size, self.spritesheet, True))
				elif tile == '2':
					tiles.append(Tile('dirt3.png', x * self.tile_size, y * self.tile_size, self.spritesheet, True))
					# Move to next tile in current row
				x += 1

			# Move to next row
			y += 1
			# Store the size of the tile map
		self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
		return tiles




