#This is gamesetting.py - contains global settings for the Bomberman game

# A common, game-friendly default resolution that fits most laptops nicely
SCREENWIDTH = 1280
SCREENHEIGHT = 720



# GAME FRAMES PER SECONDS
FPS = 60

# Y COORDINATE OFFSET FOR SPRITES
Y_OFFSET = 92


# ACTUAL SPRITE SIZE FROM YOUR SHEET
SPRITE_WIDTH = 32   # Most common size for this style
SPRITE_HEIGHT = 32

# TILE SIZE FROM YOUR TILE SHEET
TILE_WIDTH = 32
TILE_HEIGHT = 32

# GAME MATRIX 
SIZE = 64  # SIZE OF EACH TILE IN PIXELS
# Increase the level size so the world is larger than the screen
# This allows the camera to scroll when the player moves around
ROWS = 20
COLS = 40


# COLOURS
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (188, 188, 188)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
LIGHTGREEN = (144, 238, 144)
DARKGREY = (64, 64, 64)
LIGHTGREY = (192, 192, 192)

#COLOR PALLETE
YELLOW_WHITE = (254,255,211)
PITCH_RED = (219,76,76)
YELLOWISH = (253, 228, 188)
PURPLEISH = (95,107,210)
DARK_RED = (97,25,19)

# SPRITE COORDINATES

PLAYER = {
    # Row 0: Walking
    "walk_down": [(0, 0), (0, 1), (0, 2)], 
    "walk_left": [(3, 0), (3, 1), (3, 2)],
    "walk_right": [(1, 0), (1, 1), (1, 2)],
    "walk_up": [(2, 0), (2, 1), (2, 2)],

    # Row 2: Idling (Assuming these are the stand-still frames)
    "idle_down": [(2, 3)],
    "idle_left": [(2, 0)],
    "idle_right": [(2, 6)],
    "idle_up": [(2, 9)],
    
    # Row 1: Dead/Vulnerable (Adjusting based on observation)
    "dead_anim": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)], 
    
    # Row 3: Bomb/Kick Animation (Example)
    "kick_anim": [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)],
    
    # Row 4: Happy/Win
    "win_anim": [(4, 0), (4, 1), (4, 2), (4, 3)],
    
    # Row 5: Sleep
    "sleep_anim": [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4)],
}

#HARD_BLOCK = {"hard_block":[(0,2)]}
#HARD_BLOCK = {"hard_block":[(0,1)]} #before  [(0.2,1.2)]}
HARD_BLOCK = {"hard_block":[(0,1)]}
SOFT_BLOCK = {"soft_block":[(0,7)]} #block for purple soft block [(0,7]}