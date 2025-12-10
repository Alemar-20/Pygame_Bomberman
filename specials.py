import pygame
import gamesetting as gs

class Special(pygame.sprite.Sprite):
  def __init__(self, game, images,name, group, type, row_num, col_num, size):
    super().__init__(group)
    self.GAME = game
    self.type = type

    self.name = name

    # Level Matrix position
    self.row = row_num
    self.col = col_num

    # Spaw Coordinates of special
    self.size = size
    self.x = self.col * self.size
    self.y = (self.row * self.size) + gs.Y_OFFSET

    # Special Animation and Images
    self.image = images
    self.rect = self.image.get_rect(topleft=(self.x, self.y))

  def update(self):
    pass
  def draw (self, window, x_offset=0, y_offset=0):
    window.blit(self.image, (self.rect.x - x_offset, self.rect.y - y_offset))