# ============================================================================
# FILE: gamesetting.py - GLOBAL GAME CONFIGURATION AND CONSTANTS
# ============================================================================

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
# Default window resolution - fits most laptops and monitors
SCREENWIDTH = 1280   # Window width in pixels
SCREENHEIGHT = 720   # Window height in pixels (default 720)

# Target frame rate for consistent game speed across all devices
FPS = 60  # Frames per second - controls game update frequency

# Vertical offset for positioning info panel and game world
Y_OFFSET = 92  # Pixels from top of screen where game world starts (leaves room for info panel)

# ============================================================================
# GAMEPLAY SETTINGS
# ============================================================================
# Time limit for each stage in seconds (countdown timer)
STAGE_TIME = 200  # Seconds per stage - when timer hits 0, enemies spawn

# ============================================================================
# ENEMY ATTRIBUTES - Defines behavior for each enemy type
# ============================================================================
# Dictionary mapping enemy names to their characteristics:
# - speed: Movement speed multiplier (0.5 = slow, 4 = very fast)
# - wall_hack: Can pass through soft blocks if True
# - chase_player: Will actively pursue player if True
# - LoS: Line of sight range in tiles (0 = no vision check)
# - see_player_hack: Can see player through walls if True
# Enemy Attributes
ENEMIES = {
    "ballom":  {"speed": 1,   "wall_hack": False, "chase_player": False, "LoS": 0,  "see_player_hack": False},  # Basic enemy - slow, random movement
    "onil":    {"speed": 2,   "wall_hack": False, "chase_player": True,  "LoS": 4,  "see_player_hack": False},  # Fast chaser with short vision
    "dahl":    {"speed": 2,   "wall_hack": False, "chase_player": True,  "LoS": 0,  "see_player_hack": False},  # Fast chaser, no vision requirement
    "minvo":   {"speed": 2,   "wall_hack": False, "chase_player": True,  "LoS": 4,  "see_player_hack": True},   # Can see through walls
    "doria":   {"speed": 0.5, "wall_hack": True,  "chase_player": True,  "LoS": 6,  "see_player_hack": True},   # Slow but passes through walls
    "ovape":   {"speed": 1,   "wall_hack": True,  "chase_player": True,  "LoS": 8,  "see_player_hack": False},  # Moderate speed, wall-passing
    "pass":    {"speed": 2,   "wall_hack": True,  "chase_player": True,  "LoS": 12, "see_player_hack": False},  # Fast wall-passer with good vision
    "pontan":  {"speed": 4,   "wall_hack": True,  "chase_player": True,  "LoS": 30, "see_player_hack": False}   # Very fast, spawns when timer reaches 0
}

# ============================================================================
# SPRITE AND TILE DIMENSIONS
# ============================================================================
# Original sprite dimensions from the sprite sheet
SPRITE_WIDTH = 32    # Width of each sprite frame in pixels
SPRITE_HEIGHT = 32   # Height of each sprite frame in pixels``

# Tile dimensions for background tiles
TILE_WIDTH = 32      # Width of background tile in pixels
TILE_HEIGHT = 32     # Height of background tile in pixels

# ============================================================================
# GAME WORLD DIMENSIONS
# ============================================================================
SIZE = 64  # Size of each game tile/cell when scaled (64x64 pixels)
           # Sprites are scaled from 32x32 to 64x64 for better visibility

# Level grid dimensions - larger than screen to enable camera scrolling
ROWS = 20  # Number of rows in the level grid (vertical tiles)
COLS = 30  # Number of columns in the level grid (horizontal tiles)
           # Total world size: 1920x1280 pixels (30*64 x 20*64)

# ============================================================================
# COLOR PALETTE
# ============================================================================
# Standard RGB colors used throughout the game
BLACK = (0, 0, 0)           # Used for colorkey transparency and backgrounds
RED = (255, 0, 0)           # Bright red
WHITE = (255, 255, 255)     # Pure white
GREEN = (0, 255, 0)         # Bright green
BLUE = (0, 0, 255)          # Bright blue
YELLOW = (255, 255, 0)      # Bright yellow
GREY = (188, 188, 188)      # Medium grey
ORANGE = (255, 165, 0)      # Orange
PURPLE = (128, 0, 128)      # Purple
BROWN = (165, 42, 42)       # Brown
PINK = (255, 192, 203)      # Light pink
CYAN = (0, 255, 255)        # Cyan
LIGHTGREEN = (144, 238, 144) # Light green
DARKGREY = (64, 64, 64)     # Dark grey
LIGHTGREY = (192, 192, 192) # Light grey

# Custom color palette for game aesthetics
YELLOW_WHITE = (254, 255, 211)  # Pale yellow-white
PITCH_RED = (219, 76, 76)       # Deep red
YELLOWISH = (253, 228, 188)     # Cream/beige
PURPLEISH = (95, 107, 210)      # Purple-blue
DARK_RED = (97, 25, 19)         # Very dark red (background color)

# ============================================================================
# SPRITE SHEET COORDINATES
# ============================================================================
# All sprite coordinates are stored as (row, column) tuples representing
# their position on the sprite sheet. Each sprite is 32x32 pixels on the sheet.
# These coordinates are used by the Assets class to extract sprites.
# ============================================================================

# PLAYER CHARACTER SPRITE COORDINATES
PLAYER = {
    # Walking animations - 3 frames each for smooth movement
    "walk_down":  [(0, 0), (0, 1), (0, 2)],  # Player walking downward
    "walk_left":  [(3, 0), (3, 1), (3, 2)],  # Player walking left
    "walk_right": [(1, 0), (1, 1), (1, 2)],  # Player walking right
    "walk_up":    [(2, 0), (2, 1), (2, 2)],  # Player walking upward

    # Idle/standing still - single frame for each direction
    "idle_down":  [(0, 0)],  # Facing down
    "idle_left":  [(3, 0)],  # Facing left
    "idle_right": [(1, 0)],  # Facing right
    "idle_up":    [(2, 0)],  # Facing up
    
    # Death animation - 9 frames showing player being defeated
    "dead_anim": [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)], 
    
    # Bomb kick animation - 7 frames
    "kick_anim": [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)],
    
    # Victory/happy animation - 7 frames shown when level is completed
    "win_anim": [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7)],
    
    # Sleep/idle animation - 8 frames when player is inactive
    "sleep_anim": [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)],
}

# BLOCK SPRITE COORDINATES
HARD_BLOCK = {"hard_block": [(2, 1)]}  # Indestructible wall blocks
SOFT_BLOCK = {"soft_block": [(0, 0), (0, 1), (0, 2), (0, 3),  # Destructible blocks with
                             (1, 0), (1, 2), (1, 3), (1, 4),  # multiple destruction frames
                             (2, 0), (2, 1), (2, 2)]}

# BOMB SPRITE COORDINATES - 4-frame pulsing animation
BOMB = {"bomb": [(0, 0), (0, 1), (0, 2), (0, 1)]}

# EXPLOSION SPRITE COORDINATES - Different sprites for each direction
EXPLOSION = {
    "centre":     [(2, 7), (2, 8), (2, 9), (2, 10)],   # Center of explosion (where bomb was)
    "left_end":   [(3, 0), (3, 1), (3, 2), (3, 3)],    # Left end of flame (edge)
    "right_end":  [(3, 0), (3, 1), (3, 2), (3, 3)],    # Right end of flame (edge)
    "up_end":     [(4, 0), (4, 1), (4, 2), (4, 3)],    # Upward end of flame (edge)
    "down_end":   [(4, 0), (4, 1), (4, 2), (4, 3)],    # Downward end of flame (edge)
    "left_mid":   [(3, 4), (3, 5), (3, 6), (3, 7)],    # Horizontal mid-section (left direction)
    "right_mid":  [(3, 4), (3, 5), (3, 6), (3, 7)],    # Horizontal mid-section (right direction)
    "up_mid":     [(4, 4), (4, 5), (4, 6), (4, 7)],    # Vertical mid-section (up direction)
    "down_mid":   [(4, 4), (4, 5), (4, 6), (4, 7)],    # Vertical mid-section (down direction)
}
# ENEMY SPRITE COORDINATES - Each enemy has walk and death animations
# Walk animations use 3 frames, death animations use 5 frames

# Ballom - Basic slow enemy with random movement
BALLOM = {
    "walk_right": [(5, 0), (5, 1), (5, 2)],
    "walk_down":  [(5, 0), (5, 1), (5, 2)],
    "walk_left":  [(5, 3), (5, 4), (5, 5)],
    "walk_up":    [(5, 3), (5, 4), (5, 5)],
    "death":      [(5, 6), (5, 7), (5, 8), (5, 9), (5, 10)],
}

# Onil - Fast enemy with short line of sight
ONIL = {
    "walk_right": [(8, 0), (8, 1), (8, 2)],
    "walk_down":  [(8, 0), (8, 1), (8, 2)],
    "walk_left":  [(8, 3), (8, 4), (8, 5)],
    "walk_up":    [(8, 3), (8, 4), (8, 5)],
    "death":      [(8, 6), (8, 7), (8, 8), (8, 9), (8, 10)],
}

# Dahl - Fast chaser with no vision requirement
DAHL = {
    "walk_right": [(10, 0), (10, 1), (10, 2)],
    "walk_down":  [(10, 0), (10, 1), (10, 2)],
    "walk_left":  [(10, 3), (10, 4), (10, 5)],
    "walk_up":    [(10, 3), (10, 4), (10, 5)],
    "death":      [(10, 6), (10, 7), (10, 8), (10, 9), (10, 10)],
}

# Minvo - Can see through walls
MINVO = {
    "walk_right": [(6, 0), (6, 1), (6, 2)],
    "walk_down":  [(6, 0), (6, 1), (6, 2)],
    "walk_left":  [(6, 3), (6, 4), (6, 5)],
    "walk_up":    [(6, 3), (6, 4), (6, 5)],
    "death":      [(6, 6), (6, 7), (6, 8), (6, 9), (6, 10)],
}

# Doria - Slow but passes through walls
DORIA = {
    "walk_right": [(9, 0), (9, 1), (9, 2)],
    "walk_down":  [(9, 0), (9, 1), (9, 2)],
    "walk_left":  [(9, 3), (9, 4), (9, 5)],
    "walk_up":    [(9, 3), (9, 4), (9, 5)],
    "death":      [(9, 6), (9, 7), (9, 8), (9, 9), (9, 10)],
}

# Ovape - Moderate speed wall-passer
OVAPE = {
    "walk_right": [(11, 0), (11, 1), (11, 2)],
    "walk_down":  [(11, 0), (11, 1), (11, 2)],
    "walk_left":  [(11, 3), (11, 4), (11, 5)],
    "walk_up":    [(11, 3), (11, 4), (11, 5)],
    "death":      [(11, 6), (11, 7), (11, 8), (11, 9), (11, 10)],
}

# Pass - Fast wall-passer with good vision
PASS = {
    "walk_right": [(7, 0), (7, 1), (7, 2)],
    "walk_down":  [(7, 0), (7, 1), (7, 2)],
    "walk_left":  [(7, 3), (7, 4), (7, 5)],
    "walk_up":    [(7, 3), (7, 4), (7, 5)],
    "death":      [(7, 6), (7, 7), (7, 8), (7, 9), (7, 10)],
}

# Pontan - Very fast enemy that spawns when timer reaches 0
PONTAN = {
    "walk_right": [(5, 11), (6, 11), (7, 11), (8, 11)],  # 4-frame animation
    "walk_down":  [(5, 11), (6, 11), (7, 11), (8, 11)],
    "walk_left":  [(5, 11), (6, 11), (7, 11), (8, 11)],
    "walk_up":    [(5, 11), (6, 11), (7, 11), (8, 11)],
    "death":      [(9, 11), (5, 7), (5, 8), (5, 9), (5, 10)],
}
# POWER-UP/SPECIAL ITEM SPRITE COORDINATES
# Each power-up is a single sprite that appears when soft blocks are destroyed
SPECIALS = {
    "bomb_up":     [(3, 8)],   # Increases max bomb capacity by 1
    "fire_up":     [(3, 9)],   # Increases explosion range by 1
    "speed_up":    [(3, 10)],  # Increases player movement speed
    "wall_hack":   [(3, 11)],  # Allows player to walk through soft blocks
    "remote":      [(4, 8)],   # Enables remote detonation of bombs
    "bomb_pass":   [(4, 9)],   # Allows player to walk through bombs
    "flame_pass":  [(4, 10)],  # Makes player immune to explosions
    "invisible":   [(4, 11)],  # Makes player temporarily invisible to enemies
    "exit":        [(1, 11)],  # Level exit door (spawns 10 pontan enemies when hit)
}

# SPECIAL-TO-ENEMY CONNECTIONS
# Maps which enemy drops which power-up (used for spawning logic)
SPECIAL_CONNECTIONS = {
    "bomb_up":     "ballom",   # Ballom drops bomb_up
    "fire_up":     "onil",     # Onil drops fire_up
    "speed_up":    "dahl",     # Dahl drops speed_up
    "wall_hack":   "minvo",    # Minvo drops wall_hack
    "remote":      "doria",    # Doria drops remote
    "bomb_pass":   "ovape",    # Ovape drops bomb_pass
    "flame_pass":  "pass",     # Pass drops flame_pass
    "invisible":   "pontan",   # Pontan drops invisible
    "exit":        "pontan",   # Exit spawns pontan enemies
}

# ============================================================================
# UI TEXT AND NUMBER SPRITES
# ============================================================================
# Text labels displayed in the info panel
TIME_WORD = {"time_word": [(13, 4)]}    # "TIME" text (80px wide)
LEFT_WORD = {"left_word": [(13, 0)]}    # "LEFT" text (64px wide)
STAGE_WORD = {"stage_word": [(14, 0)]}  # "STAGE" text (80px wide)

# Number sprites for displaying scores, timer, and lives
# Black numbers used in info panel against light backgrounds
NUMBERS_BLACK = {
    0: [(12, 10)], 1: [(12, 11)], 2: [(13, 8)],
    3: [(13, 9)],  4: [(13, 10)], 5: [(13, 11)],
    6: [(14, 8)],  7: [(14, 9)],  8: [(14, 10)],
    9: [(14, 11)]
}

# White numbers used for contrast or special displays
NUMBERS_WHITE = {
    0: [(14, 5)], 1: [(14, 6)], 2: [(14, 7)],
    3: [(15, 5)], 4: [(15, 6)], 5: [(15, 7)],
    6: [(15, 8)], 7: [(15, 9)], 8: [(15, 10)],
    9: [(15, 11)]
}

# Score popup images that appear when enemies are destroyed
# Maps score values to their sprite coordinates
SCORE_IMAGES = {
    100:  [(12, 6)],    200:  [(12.5, 6)],
    400:  [(12, 7)],    800:  [(12.5, 7)],
    1000: [(12, 8)],    2000: [(12.5, 8)],
    4000: [(12, 9)],    8000: [(12.5, 9)]
}

# ============================================================================
# ENEMY SCORE VALUES
# ============================================================================
# Points awarded for defeating each enemy type
SCORES = {
    "ballom":  100,  # Basic enemy
    "onil":    100,  # Fast chaser
    "dahl":    200,  # Fast chaser
    "minvo":   200,  # Wall-vision enemy
    "doria":   400,  # Wall-passing enemy
    "ovape":   400,  # Wall-passing enemy
    "pass":    800,  # Fast wall-passer
    "pontan":  800   # Very fast time-out enemy
}

# ============================================================================
# SOUND FILE NAMES
# ============================================================================
# List of all sound effect and music files to be loaded
SOUNDS = [
    "Bomberman SFX (1).wav",       # Sound effect 1
    "Bomberman SFX (2).wav",       # Sound effect 2
    "Bomberman SFX (3).wav",       # Sound effect 3
    "Bomberman SFX (4).wav",       # Sound effect 4
    "Bomberman SFX (5).wav",       # Sound effect 5
    "Bomberman SFX (6).wav",       # Sound effect 6
    "Bomberman SFX (7).wav",       # Sound effect 7
    "BM - 01 Title Screen.mp3",    # Title screen music
    "BM - 02 Stage Start.mp3",     # Level start jingle
    "BM - 03 Main BGM.mp3",        # Main gameplay music
    "BM - 04 Power-Up Get.mp3",    # Power-up pickup sound
    "BM - 05 Stage Clear.mp3",     # Level complete music
    "BM - 07 Special Power-Up Get.mp3",  # Special item pickup sound
    "BM - 09  Miss.mp3"            # Player death sound
]