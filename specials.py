import pygame
import gamesetting as gs
from info_panel import Scoring

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
                              "invisible": self.invisible_special,
                              "exit": self.end_stage # Exit handled in game.py
                             }
    self.score = 1000 if self.name == "exit" else 500

  def update(self):
      if self.GAME.PLAYER.rect.collidepoint(self.rect.center):
         # activate power up
         self.power_up_activate[self.name](self.GAME.PLAYER)
         if self.name == "exit":
            self.GAME.bg_music.stop()
            self.GAME.bg_music_special.stop()
            self.GAME.PLAYER.update_score(self.score)
            return
         self.GAME.level_matrix[self.row][self.col] = "_"
         self.GAME.ASSETS.sounds["Bomberman SFX (4).wav"].play()
         self.GAME.bg_music.stop()
         self.GAME.bg_music_special.play(loops=-1)
         self.kill()
         self.GAME.PLAYER.update_score(self.score)
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

  def end_stage(self, player):
     """end the level, and generate a new level"""
     if len(self.GAME.groups["enemies"].sprites()) > 0:
        return
     
     self.GAME.new_stage()

  def hit_by_explosion(self):
      """Action to take is special item is hit by an explosion"""

      enemies = []
      for _ in range(10):
         enemies.append(gs.SPECIAL_CONNECTIONS[self.name])

      self.GAME.insert_enemies_into_level(self.GAME.level_matrix, enemies)   
      self.GAME.level_matrix[self.row][self.col] = "_"
      self.kill()  