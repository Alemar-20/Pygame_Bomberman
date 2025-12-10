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


    # Power Up Abilities
    self.power_up_activate = {"bomb_up": self.bomb_up_special,
                              "fire_up": self.fire_up_special,
                              "speed_up": self.speed_up_special,
                              "wall_hack": self.wall_hack_special,
                              "remote": self.remote_special,
                              "bomb_pass": self.bomb_hack_special,
                              "flame_pass": self.flame_pass_special,
                              "invisible": self.invisible_special
                             }


  def update(self):
      if self.GAME.PLAYER.rect.collidepoint(self.rect.center):
         # activate power up
         self.power_up_activate[self.name](self.GAME.PLAYER)
         self.GAME.level_matrix[self.row][self.col] = "_"
         self.kill()
         return
  def draw (self, window, x_offset=0, y_offset=0):
    window.blit(self.image, (self.rect.x - x_offset, self.rect.y - y_offset))

  def bomb_up_special(self,player):
     # Increase player's bomb limit by 1
     player.bomb_limit += 1  

  def fire_up_special(self, player):
     # Increase player's bomb explosion power by 1
     player.power += 1

  def speed_up_special(self, player):
     # Increase player's movement speed by 1
     player.speed += 1
  def wall_hack_special(self, player): 
     # Turn on the player wall hack  
     player.wall_hack = True

  def remote_special(self, player):
     # Give player remote bomb detonation ability
     player.remote = True

  def bomb_hack_special(self, player):
     # Give player bomb hack ability
     player.bomb_hack = True

  def flame_pass_special(self, player):
     # Give player ability to ignore bomb blasts
     player.flame_pass = True

  def invisible_special(self, player):
     # Make player invisible to enemies
     player.invisibility = True
     player.invisibility_timer = pygame.time.get_ticks()


