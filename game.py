#This is game.py - the main game logic for Bomberman
import pygame
from character import Character
from enemy import Enemy
from blocks import Hard_block, Soft_Block, Special_Soft_Block
from random import choice, randint
from info_panel import InfoPanel
from specials import Special
import gamesetting as gs

# ============================================================================
# FILE: game.py - CORE GAME LOGIC AND STATE MANAGEMENT
# ============================================================================
# PURPOSE:
#   Manages all game logic including:
#   - Level generation and block placement (hard and soft blocks)
#   - Game state updates (sprite updates, camera interpolation)
#   - Camera system with deadzone and smooth following
#   - Rendering of game world (background, sprites, camera offsets)
#
# DEPENDENCIES:
#   - pygame: Sprite groups, rendering
#   - Character: Player sprite class
#   - Hard_block, Soft_Block: Block sprite classes
#   - gamesetting: Game configuration and constants
# ============================================================================

# ============================================================================
# CLASS: Game - Main game state and logic controller
# ============================================================================
class Game:
  def __init__(self, main, assets):
    """
    CONSTRUCTOR - Initialize game state and world
    
    INITIALIZATION STEPS:
    1. Store references to main Bomberman instance and Assets
    2. Create sprite groups for organizing game objects
    3. Create the player character at starting position (row 3, col 2)
    4. Initialize camera system with offsets and smoothing parameters
    5. Generate the level matrix and populate with blocks
    """
    # LINK WITH MAIN CLASS AND ASSETS
    self.MAIN = main
    self.ASSETS = assets

    # Sprite groups for organizing and updating game objects
    self.groups = {
      "hard_block": pygame.sprite.Group(),    # Static indestructible barriers
      "soft_block": pygame.sprite.Group(),    # Destructible blocks
      "bomb": pygame.sprite.Group(),          # Bombs placed by player
      "specials" : pygame.sprite.Group(),      # Special items/power-ups
      "explosion": pygame.sprite.Group(),     # Explosion effects
      "enemies": pygame.sprite.Group(),      # Enemy characters
      "player": pygame.sprite.Group()         # Player character
    }
    
    # Create player character at starting position (grid: row 3, col 2)
    self.PLAYER = Character(self, self.ASSETS.player_char, self.groups["player"], 3, 2, gs.SIZE)
    

    # CAMERA SYSTEM - Smooth following with deadzone
    # Current camera offsets (in pixels) - what's actually rendered
    self.x_camera_offset = 0
    self.y_camera_offset = 0
    
    # Target camera offsets - where camera wants to be
    self.cam_target_x = 0
    self.cam_target_y = 0
    
    # Camera lerp: how quickly camera follows (0.14 = smooth, slower follow)
    # Lower values = smoother, slower follow. Higher values = snappier, more direct follow
    self.camera_lerp = 0.14
    
    # Deadzone ratio: Fraction of screen where player can move without camera moving
    # 0.6 = 60% of screen (centered) is the deadzone
    # Camera only moves when player leaves this central area
    self.deadzone_ratio = 0.6
    
    # LEVEL INFORMATION
    self.level = 1
    self.level_special = self.select_a_special()
    self.level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)
    self.level_info = InfoPanel(self, self.ASSETS)

  def input(self, events):
    # Expect an events list forwarded from main
    self.PLAYER.input(events)
    
  def update(self):
    # Update info panel 
    self.level_info.update()
    # self.hard_blocks.update()
    # self.soft_block.update()
    # self.PLAYER.update()
    for value in self.groups.values():
      for item in value:
        item.update()
    # Perform enemy collision check with explosions, only if there is an explosion
    if self.groups["explosion"]:
      # Compare explosion group with the enemies group, check for collision. This will retrun a dictionary
      # keys: group 1, values: list of all group 2 that collision detection occurs
      killed_enemies = pygame.sprite.groupcollide(self.groups["explosion"],
                                                   self.groups["enemies"], False, False)
      if killed_enemies:
         # Cycle through the dictionary, performing checks on each enemy colliding with a flame
         for flame, enemies in killed_enemies.items():
           # Cycle through each enemy in the dictionary value list
           for enemy in enemies:
             if pygame.sprite.collide_mask(flame,enemy):
               enemy.destroy()



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
    window.fill(gs.DARK_RED)
    #This is from gemini as a test

    # Draw information panel to screen
    self.level_info.draw(window)

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
    self.insert_power_up_into_matrix(matrix, self.level_special)
    self.insert_power_up_into_matrix(matrix, "exit")
    self.insert_enemies_into_level(matrix)
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
  def insert_power_up_into_matrix(self,matrix, special):
      """Randomly insert the special Block into the level matrix"""
      power_up = special
      valid = False
      while not valid:
        row = randint(0, gs.ROWS - 1)
        col = randint(0, gs.COLS - 1)
        if row == 0 or row == len(matrix) - 1 or col == 0 or col == len(matrix[0]) - 1:
          continue
        elif row % 2 == 0 and col % 2 == 0:
          continue
        elif row in [2,3,4] and col in [1,2,3]:
          continue
        elif matrix[row][col] != "_":
          continue
        else:
          valid = True
      cell = Special_Soft_Block(self,
                                self.ASSETS.soft_block["soft_block"],
                                self.groups["soft_block"],
                                row, col, power_up)   
      matrix[row][col] = cell 

  def insert_enemies_into_level(self,matrix, enemies=None):
    """Randomly insert enemies into the level matrix, using level matrix for valid locations"""
    enemies_list = self.select_enemies_to_spawn() if enemies == None else enemies
    print(enemies_list)
    # Get grid coordinates of the player character
    pl_col = self.PLAYER.col_num
    pl_row = self.PLAYER.row_num

    # Load in the enemies
    for enemy in enemies_list:
        valid_choice = False
        while not valid_choice:
          row = randint(0, gs.ROWS - 1)
          col = randint(0, gs.COLS - 1)

          # Check if this row/col within 3 blocks of the player
          if row in [pl_row - 3, pl_row - 2, pl_row - 1, pl_row, pl_row + 1, pl_row + 2, pl_row + 3] and \
             col in [pl_col - 3, pl_col - 2, pl_col - 1, pl_col, pl_col + 1, pl_col + 2, pl_col + 3]:
             continue
          
          elif matrix[row][col] == "_":
            valid_choice = True
            Enemy(self, self.ASSETS.enemies[enemy], self.groups["enemies"], enemy, row, col, gs.SIZE)
          else:
            continue

  def regenerate_stage(self):
    """Restart state/level"""        
    # Clear all object from the various pygame, groups, excepet the player
    for key in self.groups.keys():
      if key == "player":
        continue
      self.groups[key].empty()
    
    # Clear the level matrix
    self.level_matrix.clear()
    self.level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)

    # Reset the camera x position back to zerro
    self.camera_x_offset = 0

  def select_enemies_to_spawn(self):
    """Generate a list of enemies to spawn"""  
    enemies_list = []
    enemies = {0: "ballom", 1: "ballom", 2: "onil", 3: "dahl", 4: "minvo",
               5: "doria", 6: "ovape", 7: "pass", 8: "pontan"}

    if self.level <= 8:
      self.add_enemies_to_list(8,2,0, enemies, enemies_list)  #gawin 8,2,3 mamaya
    elif self.level <= 17:
      self.add_enemies_to_list(7,2,1, enemies, enemies_list)
    elif self.level <= 17:
       self.add_enemies_to_list(6,3,2, enemies, enemies_list)
    elif self.level <= 26:
       self.add_enemies_to_list(7,2,1, enemies, enemies_list)
    elif self.level <= 35:
       self.add_enemies_to_list(5,3,2, enemies, enemies_list)   
    elif self.level <= 45:
       self.add_enemies_to_list(4,4,2, enemies, enemies_list)
    else:
      self.add_enemies_to_list(3,4,4, enemies, enemies_list)
    return enemies_list    

  def add_enemies_to_list(self, num_1, num_2, num_3, enemies, enemies_list):
      for num in range(num_1):
        enemies_list.append("ballom")
      for num in range(num_2):
        enemies_list.append(enemies[self.level % 9])  
      for num in range(num_3):
        enemies_list.append(choice(list(enemies.values()))) 
      return   
  
  def select_a_special(self):
    special = list(gs.SPECIALS.keys())
    special.remove("exit")
    if self.level == 4:
      power_up = "speed_up"
    elif self.level == 1:
      power_up = "bomb_up"
    elif self.PLAYER.bomb_limit <= 2 or self.player.power <= 2:
      power_up = choice (["bomb_up", "fire_up"])
    else:
      if self.player.wall_hack:
        special.remove("wall_hack")
      if self.player.remote.detonate:
        special.remove("remote")    
      if self.player.bomb_hack:
        special.remove("bomb_pass") 
      if self.player.flame_hack:
        special.remove("flame_pass")    
      if self.player.bomb_limit == 10:
        special.remove("bomb_up")
      if self.player.power == 10:
        special.remove("fire_up")
      power_up = choice(special) 
    return power_up       


  def new_stage(self):
    """Increase the stage level number, and selects a new level specials"""
    self.level += 1
    self.level_special = self.select_a_special()
    self.PLAYER.set_player_position()
    self.PLAYER.set_player_images()
    self.regenerate_stage()
    print(self.level)