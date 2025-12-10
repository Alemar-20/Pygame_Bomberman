# ============================================================================
# FILE: character.py - PLAYER CHARACTER CLASS
# ============================================================================
# PURPOSE:
#   Defines the Character class representing the player in the game.
#   Handles:
#   - Character movement (WASD / Arrow keys) with collision detection
#   - Animation frame switching based on movement direction
#   - Camera follow system
#   - Input processing
#
# DEPENDENCIES:
#   - pygame: Sprite and rendering
#   - gamesetting: Game configuration and tile sizes
# ============================================================================

#This is character.py - defines the Character class for the Bomberman game
from tokenize import group
import pygame
import gamesetting as gs

# Import block classes for collision detection in explosion spreading
from blocks import Hard_block, Soft_Block

# ============================================================================
# CLASS: Character - Player sprite with movement, animation, and collision
# ============================================================================
class Character(pygame.sprite.Sprite):
    def __init__(self, game, image_dict, group, row_num, col_num, size):
        """
        CONSTRUCTOR - Initialize the player character
        
        PARAMETERS:
        - game: Game object reference for camera updates and collision checks
        - image_dict: Dictionary of animation frames indexed by direction (walk_left, walk_right, etc.)
        - group: Pygame sprite group for rendering
        - row_num: Starting grid row position
        - col_num: Starting grid column position
        - size: Tile size in pixels (64px)
        
        INITIALIZATION STEPS:
        1. Call parent Sprite constructor to add to sprite group
        2. Store references to game and grid position
        3. Calculate pixel position from grid position
        4. Initialize animation state and frame tracking
        5. Create hitbox (collision rectangle) smaller than visual sprite
        """
        super().__init__(group)
        self.GAME = game

        # Level matrix position (in grid tiles)
        self.row_num = row_num
        self.col_num = col_num
        self.size = size

        # CHARACTER WORLD POSITION (in pixels, with Y offset for visual alignment)
        self.x = self.col_num * self.size 
        self.y = (self.row_num * self.size) + gs.Y_OFFSET

        self.set_player(image_dict)

        self.lives = 3

    def input(self, events):
        """
        INPUT HANDLER - Process keyboard input for player movement
        
        HANDLES:
        - Event loop for QUIT and ESCAPE events (passed from main)
        - Continuous key polling for smooth movement (WASD / Arrow keys)
        
        MOVEMENT CONTROLS:
        - W / UP ARROW: Move up (walk_up animation)
        - A / LEFT ARROW: Move left (walk_left animation)
        - S / DOWN ARROW: Move down (walk_down animation)
        - D / RIGHT ARROW: Move right (walk_right animation)
        
        NOTES:
        - Events are passed from Bomberman.input() via Game.input()
        - Continuous polling with pygame.key.get_pressed() ensures smooth movement
        - Each movement calls self.move() which handles collision detection
        """
        # Process events passed from main (QUIT/ESCAPE)
        for event in events:
            if event.type == pygame.QUIT:
                self.GAME.MAIN.running = False  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.GAME.MAIN.running = False
                elif event.key == pygame.K_SPACE:
                    row, col, = ((self.rect.centery - gs.Y_OFFSET)//gs.SIZE, self.rect.centerx // gs.SIZE)
                    if self.GAME.level_matrix[row][col] == "_" and self.bomb_planted < self.bomb_limit:
                        Bomb(self.GAME, self.GAME.ASSETS.bomb["bomb"], 
                             self.GAME.groups["bomb"], self.power ,row, col, gs.SIZE, self.remote)  
                        print(self.bomb_planted)
                elif event.key == pygame.K_LCTRL and self.remote and self.GAME.groups["bomb"]:
                    bomb_list = self.GAME.groups["bomb"].sprites()
                    bomb_list[-1].explode()

        # Continuous key polling for smooth movement
        keys_pressed = pygame.key.get_pressed() 
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.move("walk_right")
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.move("walk_left")
        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.move("walk_up")
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.move("walk_down")

    def update(self):
        """
        UPDATE - Update sprite state each frame (currently empty as movement is
        handled in move() and animation in animate())
        """
        # if there are flame/explosion, then perform a collision check
        if len(self.GAME.groups["explosion"]) > 0:
            self.deadly_collision(self.GAME.groups["explosion"])

        # Perform collision detection with enemies
        self.deadly_collision(self.GAME.groups["enemies"])

        # Play death animation if not alive
        if self.action == "dead_anim":
            self.animate(self.action)
            if self.index == len(self.image_dict[self.action]) - 1:
                self.reset_player()
                return    

    def draw(self, window, x_offset=0, y_offset=0):
        """
        DRAW - Render the character sprite to screen with camera offset applied
        
        PARAMETERS:
        - window: pygame.Surface to draw on (the game screen)
        - x_offset: Horizontal camera offset (subtracts from x coordinate)
        - y_offset: Vertical camera offset (subtracts from y coordinate)
        
        NOTES:
        - Camera offsets shift the character position, creating the camera follow effect
        - Commented debug code shows how to draw the hitbox for debugging
        """
        window.blit(self.image, (int(self.x) - int(x_offset), int(self.y) - int(y_offset)))
        #pygame.draw.rect(window, gs.RED, self.rect, 1)

        # Optional: Uncomment to see the red hitbox for debugging
        # debug_rect = self.rect.copy()
        # debug_rect.x -= offset
        # pygame.draw.rect(window, gs.RED, debug_rect, 1)

        # # Draw the hitbox with camera offset applied (for debugging)
        debug_rect = self.rect.copy()
        debug_rect.x -= int(x_offset)
        debug_rect.y -= int(y_offset)
        pygame.draw.rect(window, gs.RED, debug_rect, 2)  # Red box, 2px thick

    def animate(self, action):
        """
        ANIMATE - Switch animation frame based on elapsed time
        
        PARAMETERS:
        - action: Current movement direction (walk_left, walk_right, walk_up, walk_down)
        
        LOGIC:
        1. Check if enough time (anim_time ms) has passed since last frame switch
        2. If yes: advance to next frame in the animation sequence
        3. Loop back to frame 0 when reaching the end of the sequence
        4. Update the current image and reset the timer
        
        NOTES:
        - Different directions have different animation sequences (defined in gamesetting.PLAYER)
        - Each direction typically has 3 frames for walking animation
        - This creates smooth sprite animation during movement
        """
        if pygame.time.get_ticks() - self.anim_time_set > self.anim_time:
            self.index += 1
            if self.index == len(self.image_dict[action]):
                self.index = 0
                if self.action == "dead_anim":
                    self.reset_player()

            #self.index = self.index % len(self.image_dict[action])
            self.image = self.image_dict[action][self.index]
            self.anim_time_set = pygame.time.get_ticks()

    def check_collision(self):
        """
        CHECK_COLLISION - Detect collisions with blocks in the game world
        
        RETURNS:
        - True: Character is colliding with a solid (non-passable) block
        - False: No collision detected
        
        COLLISION LOGIC:
        1. Get all hard blocks the character's hitbox is touching
        2. Get all soft blocks the character's hitbox is touching
        3. Combine both lists
        4. Check each block's 'passable' attribute
        5. Return True if any block has passable=False (solid wall)
        
        NOTES:
        - Uses pygame.sprite.spritecollide() for efficient collision detection
        - Hitbox is smaller than the visual sprite (inflated -20px) for better gameplay feel
        - Used in move() to prevent character from walking through walls
        """
                # 1. Get a list of all blocks we are touching
        hard_hits = pygame.sprite.spritecollide(self, self.GAME.groups["hard_block"], False)
        
        if self.bomb_hack == False:
           bomb_hits = pygame.sprite.spritecollide(self, self.GAME.groups["bomb"], False)
        
        if self.wall_hack == False:
           soft_hits = pygame.sprite.spritecollide(self, self.GAME.groups["soft_block"], False)
           if self.bomb_hack == False:
               all_hits = hard_hits + soft_hits + bomb_hits
           else:
               all_hits = hard_hits + soft_hits
        else:
           if self.bomb_hack == False:
               all_hits = hard_hits + bomb_hits
           else:
               all_hits = hard_hits

        # 2. Check each block to see if it is passable
        for block in all_hits:

            # if block in bomb_hits and hasattr(self, "bomb_hack") and self.bomb_hack:
            #     continue

            if hasattr(block, 'passable') and block.passable == False:
                return True  # We hit a solid wall!
            
        return False  # No solid collisions found


    def move(self, action):
        """
        MOVE - Handle character movement with collision detection
        
        PARAMETERS:
        - action: Direction to move (walk_left, walk_right, walk_up, walk_down)
        
        MOVEMENT LOGIC (Two-phase collision detection):
        1. PHASE 1 - Move horizontally (X axis)
           - Apply horizontal velocity (dx) based on action direction
           - Update hitbox x position
           - Check for collisions; undo movement if collision detected
        
        2. PHASE 2 - Move vertically (Y axis)
           - Apply vertical velocity (dy) based on action direction
           - Update hitbox y position
           - Check for collisions; undo movement if collision detected
        
        3. FINAL UPDATES
           - Animate the sprite based on the current action
           - Update camera position to follow the character
        
        WHY TWO PHASES?
        - Allows player to slide along walls (move diagonally if one axis is blocked)
        - More forgiving gameplay feel compared to complete rejection on collision
        
        NOTES:
        - self.speed = 3 pixels per frame
        - self.offset = 10 pixels to center the hitbox inside the sprite
        - Camera follows smoothly with interpolation (lerp) defined in Game
        """
        if not self.alive:
            return
        
        if action != self.action:
            self.action = action
            self.index = 0

        dx = 0
        dy = 0

        if action == "walk_left":
            dx = -self.speed
        elif action == "walk_right":
            dx = self.speed
        elif action == "walk_up":
            dy = -self.speed
        elif action == "walk_down":
            dy = self.speed

        # --- PHASE 1: MOVE X-AXIS ---
        self.x += dx
        # Update rect topleft to keep both X and Y in sync
        self.rect.topleft = (int(self.x + self.offset), int(self.y + self.offset))
        
        # Check collision using the new passable-aware logic
        if self.check_collision():
            self.x -= dx # Undo X movement
            self.rect.topleft = (int(self.x + self.offset), int(self.y + self.offset))

        # --- PHASE 2: MOVE Y-AXIS ---
        self.y += dy
        # Update rect topleft to keep both X and Y in sync
        self.rect.topleft = (int(self.x + self.offset), int(self.y + self.offset))
        
        # Check collision using the new passable-aware logic
        if self.check_collision():
            self.y -= dy # Undo Y movement
            self.rect.topleft = (int(self.x + self.offset), int(self.y + self.offset))

        # --- FINAL UPDATES ---
        self.animate(action)   
        
        # Update camera based on the center of the player (x and y)
        self.GAME.update_camera(self.rect.centerx, self.rect.centery)

    def set_player_position(self):
        """Character position"""   
        # Character position
        self.x = self.col_num * self.size
        self.y = (self.row_num * self.size) + gs.Y_OFFSET
    
    def set_player_images(self):
        """Character images set"""
        self.image = self.image_dict[self.action][self.index]
        self.rect = self.image.get_rect(topleft=(self.x + self.offset, self.y + self.offset))

    def set_player(self, image_dict):
         # CHARACTER ATTRIBUTES
         # starting
        self.set_player_position()
        
        self.alive = True
        self.speed = 3  # Pixels per frame when moving
        self.bomb_limit = 1
        self.remote = True
        self.power = 1
        self.wall_hack = False
        self.bomb_hack = False
        self.flame_pass = False
        



        # CHARACTER ACTION/ANIMATION STATE
        self.action = "walk_left"  # Current animation direction

        # Bomb Planted
        self.bomb_planted = 0


        # ANIMATION FRAME TRACKING
        self.index = 0  # Current frame in animation sequence
        self.anim_time = 50  # Milliseconds between frame updates
        self.anim_time_set = pygame.time.get_ticks()  # Last frame switch time
        self.image_dict = image_dict  # Dictionary of all animation sequences
        
        # Set offset BEFORE calling set_player_images (which needs it)
        shrink = 17  # Shrink 17px on each side for hitbox
        self.offset = shrink
        
        # Now create the initial image and rect
        self.set_player_images()

        # HITBOX SETUP for collision detection
        # Recalculate rect to be the proper collision hitbox (smaller than sprite)
        img_w, img_h = self.image.get_size()  # Get actual image dimensions (64x64)
        hit_w = max(1, img_w - (shrink * 2))  # Width: 64 - 34 = 30
        hit_h = max(1, img_h - (shrink * 2))  # Height: 64 - 34 = 30
        
        # Position hitbox so it's centered on (self.x, self.y)
        hit_x = int(self.x + shrink)  # Topleft X: world_x + 17
        hit_y = int(self.y + shrink)  # Topleft Y: world_y + 17
        
        self.rect = pygame.Rect(hit_x, hit_y, hit_w, hit_h)
  
    def reset_player(self):
        self.lives -= 1
        if self.lives < 0:
            self.GAME.MAIN.running = False
            return
        self.GAME.regenerate_stage()
        self.set_player(self.image_dict)

    def deadly_collision(self, group):
        if not self.alive:
            return

        for item in group:
            if not self.rect.colliderect(item.rect):
                continue    
            if pygame.sprite.collide_mask(self, item):
                self.action = "dead_anim"
                self.alive = False
                return

class Bomb(pygame.sprite.Sprite):
    def __init__(self,game, image_list, group, power, row_num, col_num, size, remote):
        super().__init__(group)
        self.GAME = game

        # Level matrix position (in grid tiles)
        self.row = row_num
        self.col = col_num

        # Coordinates
        self.size = size
        self.x = self.col * self.size
        self.y = (self.row * self.size) + gs.Y_OFFSET

        # Bomb Attributes
        self.bomb_counter = 1
        self.bomb_timer = 12    
        self.passable = True  # Bombs are passable until they explode
        self.remote = remote
        self.power = power
        self.bomb_hack = False

        # Image
        self.index = 0
        self.image_list = image_list
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Animation Settings
        self.anim_length = len(self.image_list)
        self.anim_frame_time = 200  # milliseconds per frame
        self.anim_timer = pygame.time.get_ticks()

        # Insert into level matrix
        self.insert_bomb_into_grid()

    def update(self):
        # Keep the collision rect in sync with the bomb's fixed world position.
        # Do NOT change self.x/self.y here; bombs are stationary after placement.
        self.animation()
        self.planted_bomb_player_collision()
        if self.bomb_counter == self.bomb_timer and not self.remote:
            self.explode()

        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, window, x_offset=0, y_offset=0):
        """
        DRAW - Render the bomb with camera offsets applied.

        PARAMETERS:
        - window: pygame.Surface
        - x_offset: horizontal camera offset
        - y_offset: vertical camera offset

        NOTES:
        - Use the bomb's stored world coordinates (self.x/self.y) so the bomb
          remains fixed in the world even if the player moves or the camera scrolls.
        - Keep rect synced in update(); draw only uses self.x/self.y for rendering.
        """
        window.blit(self.image, (int(self.x) - int(x_offset), int(self.y) - int(y_offset)))
    def insert_bomb_into_grid(self):
        """Add the bomb object to the level matrix"""
        self.GAME.level_matrix[self.row][self.col] = self
        self.GAME.PLAYER.bomb_planted += 1
        
    def animation(self):
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            self.index = self.index % self.anim_length
            self.image = self.image_list[self.index]
            self.anim_timer = pygame.time.get_ticks()
            self.bomb_counter += 1

    def remove_bomb_from_grid(self):
        """Remove the bomb object from the level matrix"""
        self.GAME.level_matrix[self.row][self.col] = "_"
        # OLD CODE (BUG - incremented instead of decremented):
        # self.GAME.PLAYER.bomb_planted += 1
        
        # NEW CODE (FIX - decrement to reflect bomb removal):
        self.GAME.PLAYER.bomb_planted -= 1  # Subtract 1 so player can plant again

    def explode(self):
        """Destroy the bomb and remove from the level matrix"""    
        self.kill()
        Explosion(self.GAME, self.GAME.ASSETS.explosion, "centre", self.power, 
                  self.GAME.groups["explosion"], self.row, self.col, self.size)
        
        self.remove_bomb_from_grid()

    def planted_bomb_player_collision(self):
        if not self.passable:
            return
        if not self.rect.colliderect(self.GAME.PLAYER):
            self.passable = False

    def __repr__(self):
        return "'!'"         
            
class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, image_dict, image_type, power, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game

        # Level matrix position (in grid tiles)
        self.row_num = row_num
        self.col_num = col_num

        # Sprite Coordinates
        self.size = size
        self.y = (self.row_num * self.size) + gs.Y_OFFSET
        self.x = self.col_num * self.size

        # Explosion Image and animation
        self.index = 0
        self.anim_frame_time = 75 
        self.anim_timer = pygame.time.get_ticks()

        self.image_dict = image_dict    
        self.image_type = image_type 

        self.image = self.image_dict[self.image_type][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Streng 
        self.power = power
        self.passable = False
        self.calculate_explosion_path()


    def update(self):
        self.animate()
    
    def draw(self, window, x_offset=0, y_offset=0):
        """Render explosion sprite with camera offsets applied to both axes."""
        window.blit(self.image, (int(self.x) - int(x_offset), int(self.y) - int(y_offset)))

    def animate(self):
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            if self.index == len(self.image_dict[self.image_type]):
                self.kill()
                return
            self.image = self.image_dict[self.image_type][self.index]
            self.anim_timer = pygame.time.get_ticks()        

    def calculate_explosion_path(self):
        """Explode adjacent cells, depedent on power and available cells"""        
        #                   left, right, up, down    
        valid_directions = [True, True, True, True]
        for power_cell in range(self.power):
            # Get a list of the 4 directions, tuple of cell values
            directions = self.calculate_direction_cells(power_cell)
            # Check the cells in each direction per the directions list above
            for ind, dir in enumerate (directions):
                # If the corresponding direction is still valid_directions is False, skip
                if not valid_directions[ind]:
                    continue
                # If the current cell being checked is an empty cells, check the next cell in that direction
                # To determine type of image display, wether it is a mid or end
                if self.GAME.level_matrix[dir[0]][dir[1]] == "_":
                    # If the end of the power range, use the end piece
                    if power_cell == self.power - 1:
                        FireBall(self.image_dict[dir[4]], self.GAME.groups["explosion"], dir[0], dir[1], gs.SIZE)
                    # Check if the next cell in sequence is a barrier, use end piece if true, and change valid_directions
                    # to false
                    elif self.GAME.level_matrix[dir[2]][dir[3]] in self.GAME.groups["hard_block"].sprites():
                        FireBall(self.image_dict[dir[4]], self.GAME.groups["explosion"], dir[0], dir[1], gs.SIZE)
                        valid_directions[ind] = False
                    # If next cell in sequence is not a barrier, and not the end of the flame power, use mid image
                    else:
                        FireBall(self.image_dict[dir[5]], self.GAME.groups["explosion"], dir[0], dir[1], gs.SIZE)    
                # if the current cell being checked is not empty, but is a bomb, detonate the bomb
                elif self.GAME.level_matrix[dir[0]][dir[1]] in self.GAME.groups["bomb"].sprites():
                    self.GAME.level_matrix[dir[0]][dir[1]].explode()   
                    valid_directions[ind] = False
                # If the current cell being checked is not empty, but is a soft box - destroy it
                elif self.GAME.level_matrix[dir[0]][dir[1]] in self.GAME.groups["soft_block"].sprites():
                    self.GAME.level_matrix[dir[0]][dir[1]].destroy_soft_block()
                    valid_directions[ind] = False   
                # If the current cell being checked is not empty, but is a special box
                
                # If the current cell being checked is not empty, or a bomb, or a soft block, or special
                else:
                    valid_directions[ind] = False
                    continue


    def calculate_direction_cells(self,cell):
        """Return a list of the four cells in the up and down, left and right directions"""        
        left = (self.row_num, self.col_num - (cell + 1), # Check cell immediate left
                self.row_num, self.col_num - (cell + 2), # Check cell left to that
                "left_end", "left_mid")
        right = (self.row_num, self.col_num + (cell + 1), # Check cell immediate right
                self.row_num, self.col_num + (cell + 2), # Check cell right to that
                "right_end", "right_mid")
        up = (self.row_num - (cell +1), self.col_num,  # Check all immediete up
              self.row_num - (cell + 2), self.col_num, # Check cell up to that
              "up_end", "up_mid")
        down = (self.row_num + (cell +1), self.col_num,  # Check all immediete down
              self.row_num + (cell + 2), self.col_num, # Check cell below to that
              "down_end", "down_mid")
        return [left, right, up, down]      
        
class FireBall(pygame.sprite.Sprite):
    def __init__(self, image_list, group, row_num, col_num, size):
        super().__init__(group)
        self.row_num = row_num
        self.col_num = col_num

        self.size = size

        # Coordinates
        self.y = self.row_num * self.size + gs.Y_OFFSET
        self.x = self.col_num * self.size

        # Image
        self.index = 0
        self.anim_frame_time = 75
        self.anim_timer = pygame.time.get_ticks()
        self.image_list = image_list
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.passable = False


    def update(self):
        # Keep rect synced with world position for collision detection
        self.rect.topleft = (int(self.x), int(self.y))
        self.animate()

    def draw(self, window, x_offset=0, y_offset=0):
        """Render fireball sprite with camera offsets applied to both axes."""
        window.blit(self.image, (int(self.x) - int(x_offset), int(self.y) - int(y_offset)))        

    def animate(self):
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            if self.index == len(self.image_list):
                self.kill()
                return
            self.image = self.image_list[self.index]
            self.anim_timer = pygame.time.get_ticks()
