#This is game.py - the main game logic for Bomberman
import pygame
from character import Character
from blocks import Hard_block, Soft_Block
from random import choice
import gamesetting as gs

#Hello this is a test comment for github.

class Game:
  def __init__(self, main, assets):
    # LINK WITH MAIN CLASS AND ASSETS
    self.MAIN = main
    self.ASSETS = assets

    # Player Character 
    #self.PLAYER = Character(self,self.ASSETS.player_char)

    # Groups
    # self.hard_blocks = pygame.sprite.Group()
    # self.soft_block = pygame.sprite.Group()
    self.groups = {
      "hard_block": pygame.sprite.Group(),
      "soft_block": pygame.sprite.Group(),
      "player": pygame.sprite.Group()  }
    
    # Player Character 
    self.PLAYER = Character(self,self.ASSETS.player_char, self.groups["player"],3,2,gs.SIZE)

    # Camera offsets (current and target) and smoothing
    self.x_camera_offset = 0
    self.y_camera_offset = 0
    self.cam_target_x = 0
    self.cam_target_y = 0
    # How quickly the camera follows the target (0..1). Lower = smoother/slower.
    self.camera_lerp = 0.14
    # Deadzone ratio: fraction of the screen width/height that forms the central area
    # where the player can move without moving the camera. 0.6 means 60% of the
    # screen is the deadzone; camera moves only when player leaves that area.
    self.deadzone_ratio = 0.6
    
    #Level Information
    self.level = 1
    self.level_matrix = self.generate_level_matrix(gs.ROWS,gs.COLS)

  def input(self, events):
    # Expect an events list forwarded from main
    self.PLAYER.input(events)
    
  def update(self):
    # self.hard_blocks.update()
    # self.soft_block.update()
    # self.PLAYER.update()
    for value in self.groups.values():
      for item in value:
        item.update()

    # Smoothly interpolate camera current offsets toward target offsets
    dx = self.cam_target_x - self.x_camera_offset
    dy = self.cam_target_y - self.y_camera_offset
    self.x_camera_offset += dx * self.camera_lerp
    self.y_camera_offset += dy * self.camera_lerp

  def update_camera(self, centerx, centery):
    """Update camera offsets so the player stays near screen center (both axes)."""
    total_map_width = gs.COLS * gs.SIZE
    total_map_height = gs.ROWS * gs.SIZE

    # Use current window size so camera adapts to any screen/device
    screen_w = self.MAIN.screen.get_width()
    screen_h = self.MAIN.screen.get_height()
    half_screen_w = screen_w // 2
    half_screen_h = screen_h // 2

    # Deadzone dimensions (centered). Player can move inside this rect without
    # moving the camera. Only when the player leaves it will we update camera target.
    dz_w = int(screen_w * self.deadzone_ratio)
    dz_h = int(screen_h * self.deadzone_ratio)
    dz_left = (screen_w - dz_w) / 2
    dz_right = dz_left + dz_w
    dz_top = (screen_h - dz_h) / 2
    dz_bottom = dz_top + dz_h

    # Player position relative to current camera target (screen coordinates)
    player_screen_x = centerx - self.cam_target_x
    player_screen_y = centery - self.cam_target_y

    # Determine desired_x only if player leaves deadzone horizontally
    if player_screen_x < dz_left:
      desired_x = centerx - dz_left
    elif player_screen_x > dz_right:
      desired_x = centerx - dz_right
    else:
      desired_x = self.cam_target_x

    # Determine desired_y only if player leaves deadzone vertically
    if player_screen_y < dz_top:
      desired_y = centery - dz_top
    elif player_screen_y > dz_bottom:
      desired_y = centery - dz_bottom
    else:
      desired_y = self.cam_target_y

    # Clamp to valid range based on map size and current screen size
    max_x = max(0, total_map_width - screen_w)
    max_y = max(0, total_map_height - screen_h)

    if desired_x < 0:
      desired_x = 0
    if desired_x > max_x:
      desired_x = max_x

    if desired_y < 0:
      desired_y = 0
    if desired_y > max_y:
      desired_y = max_y

    # Round targets to integer pixels to avoid half-tile cutoffs at edges
    self.cam_target_x = float(round(desired_x))
    self.cam_target_y = float(round(desired_y))

  def draw(self,window):
    #Draw the Green Background squares
    # for row_num, row in enumerate(self.level_matrix): 
    #   for col_num, in enumerate(row):
    #     window.blit(self.ASSETS.background["background"][0],
    #                 (col_num * gs.SIZE, (row_num * gs.SIZE) + gs.Y_OFFSET))

    #Fill the background entirely
    window.fill(gs.GREY)
    #This is from gemini as a test

    # Apply camera offsets to background tiles
    # Use integer offsets for drawing to prevent half-pixel tile cutoffs
    cam_x = int(round(getattr(self, 'x_camera_offset', 0)))
    cam_y = int(round(getattr(self, 'y_camera_offset', 0)))
    for row_num, row in enumerate(self.level_matrix): 
      for col_num, cell in enumerate(row): 
        # Now it unpacks correctly: col_num gets the index, 'cell' gets the value ("_" or "@")
        window.blit(self.ASSETS.background["background"][0],
                    ((col_num * gs.SIZE) - cam_x, (row_num * gs.SIZE) + gs.Y_OFFSET - cam_y))                


    # self.hard_blocks.draw(window)
    # self.soft_block.draw(window)
    # self.PLAYER.draw(window)
    # Draw all sprite groups, passing the camera offsets so sprites shift properly
    for value in self.groups.values():
      for item in value:
        # Prefer the 2-arg (x,y) draw signature; fall back for compatibility
        try:
          item.draw(window, cam_x, cam_y)
        except TypeError:
          try:
            item.draw(window, cam_x)
          except TypeError:
            item.draw(window)




  def generate_level_matrix(self,rows,cols):
    """Generate the basic level matrix"""
    matrix = []
    for row in range(rows):
      line = []
      for col in range(cols):
        line.append("_")
      matrix.append(line)
    self.insert_hard_block_into_matrix(matrix)  
    self.insert_soft_block_into_matrix(matrix)
    for row in matrix:
      print(row)
    return matrix
      

  def insert_hard_block_into_matrix(self,matrix):
    """Insert all of the Hard Barrier Block into the level of matrix"""
    LAST_ROW = len(matrix) - 1

    if not matrix or not matrix[0]:
        return
    LAST_COL = len(matrix[0]) - 1       
    
    for row_num, row in enumerate(matrix):
       for col_num, col in enumerate(row):
         
         if row_num == 0 or row_num == LAST_ROW or \
             col_num == 0 or col_num == LAST_COL or \
               (row_num % 2 == 0 and col_num % 2 == 0):
           matrix[row_num][col_num] = Hard_block(self,
                                              self.ASSETS.hard_block["hard_block"],
                                              self.groups["hard_block"],
                                              row_num, col_num)
    return
  
  def insert_soft_block_into_matrix(self,matrix):
    """RANDOMLY INSERT SOFT BLOCKS INTO THE LEVEL MATRIX"""

    for row_num, row in enumerate(matrix):
       for col_num, col in enumerate(row):
         if row_num == 0 or row_num == len(matrix) - 1 or \
            col_num == 0 or col_num == len(row) - 1 or \
            (row_num % 2 == 0 and col_num % 2 == 0):
            continue
         elif row_num in [2,3,4] and col_num in [1,2,3]:
          continue
         else:
           cell = choice(["@","_","_","_"])
           if cell == "@":
             cell = Soft_Block(self,self.ASSETS.soft_block["soft_block"],
                               self.groups["soft_block"],row_num,col_num,)
           matrix[row_num][col_num] = cell
    return     
    # for row_num, row in enumerate(matrix):
    #   for col_num, col in enumerate(row):
    #     if row_num == 0 or row_num == len(matrix)-1 or \
    #         col_num == 0 or col_num == len(row)-1 or \
    #           (row_num % 2 == 0 and col_num % 2 == 0):
    #      matrix[row_num][col_num] = Hard_block(self, # Pass the Game instance
    #                                   self.ASSETS.hard_block["hard_block"], 
    #                                   self.hard_blocks,
    #                                   row_num, col_num)
    # return           