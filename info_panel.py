import pygame
import gamesetting as gs

class InfoPanel:
  def __init__(self, game, images):
    self.GAME = game
    self.images = images


    self.black_nums = self.images.numbers_black

    # Level timer
    self.set_timer()

    # Player Lives
    self.player_lives_left_word = self.images.left_word

  def set_timer(self):
     # level timer
     self.time_total = gs.STAGE_TIME  # Total time for level in seconds
     self.timer_start = pygame.time.get_ticks()  # Start time in milliseconds
     self.time = 200

     # Images for Info Panel
     self.time_image = self.update_time_image()
     self.time_word_image = self.images.time_word
     self.time_word_rect = self.time_word_image.get_rect(topleft=(gs.SIZE, gs.SIZE // 4))

  def update_time_image(self):
    """ Update the image list for the time indicator on the info panel"""    
    num_string_list = [item for item in str(self.time)]
    images = [self.black_nums[int(image)][0] for image in num_string_list]
    return images
  
  def update(self):
    """ If timer reaches zero, stop the counter"""
    if self.time == 0:
      return
    
    # Timer countdown, change the  timer image every seconds
    if pygame.time.get_ticks() - self.timer_start >= 1000:
      self.timer_start = pygame.time.get_ticks()
      self.time -= 1
      self.time_image = self.update_time_image()
      if self.time == 0:
          self.GAME.insert_enemies_into_level(self.GAME.level_matrix, ["pontan" for _ in range(10)])

  def draw(self, window):
    # Draw the Time indicator to the screen
    window.blit(self.time_word_image, self.time_word_rect)
    start_x = 320 if len(self.time_image) == 3 else 352 if len(self.time_image) == 2 else 384
    for num, image in enumerate(self.time_image):
      window.blit(image, (start_x + (gs.SIZE * num), 16))

    # Player live left - positioned from right edge of window
    window_width = window.get_width()
    left_word_x = window_width - (gs.SIZE * 5) - 64  # LEFT word position from right
    lives_num_x = window_width - gs.SIZE - 64         # Lives number position from right
    window.blit(self.player_lives_left_word, (left_word_x, gs.SIZE // 4))  
    window.blit(self.black_nums[self.GAME.PLAYER.lives][0], (lives_num_x, gs.SIZE // 4))



