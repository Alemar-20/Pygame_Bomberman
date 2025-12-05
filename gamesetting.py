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
HARD_BLOCK = {"hard_block":[(2,1)]} #0,1 default  #0,4
SOFT_BLOCK = {"soft_block":[(0,7)]} #block for purple soft block [(0,7]}
BOMB = {"bomb": [(0,0),(0,1),(0,2),(0,1),]} #(0,4),(0,5)]}  #bomb animation frames
# OLD COORDINATES (WRONG - all pointing to same rows, no full spread):
EXPLOSION = {"centre":[(2,7),(2,8),(2,9),(2,10)],
             "left_end":[(3,0),(3,1),(3,2),(3,3)],
             "right_end":[(3,0),(3,1),(3,2),(3,3)],
             "up_end":[(4,0),(4,1),(4,2),(4,3)],
             "down_end":[(4,0),(4,1),(4,2),(4,3)],
             "left_mid":[(3,4),(3,5),(3,6),(3,7)], 
             "right_mid":[(3,4),(3,5),(3,6),(3,7)],
             "up_mid":[(4,4),(4,5),(4,6),(4,7)],
             "down_mid":[(4,4),(4,5),(4,6),(4,7)],
            }

# DEFAULT_EXPLOSION = [(0,0), (0,1), (0,2), (0,3)]

# EXPLOSION = {
#     "centre":    DEFAULT_EXPLOSION,
#     "left_end":  DEFAULT_EXPLOSION,
#     "left_mid":  DEFAULT_EXPLOSION,
#     "right_end": DEFAULT_EXPLOSION,
#     "right_mid": DEFAULT_EXPLOSION,
#     "up_end":    DEFAULT_EXPLOSION,
#     "up_mid":    DEFAULT_EXPLOSION,
#     "down_end":  DEFAULT_EXPLOSION,
#     "down_mid":  DEFAULT_EXPLOSION,
# }


# NEW COORDINATES (FIXED - full cross explosion with all directions visible):
# EXPLOSION = {"centre":[(0,0),(0,1),(0,2),(0,1)],              # Center cross (row 0, cols 0-3, 4 frames)
#              "left_end":[(1,0),(1,1),(1,2),(1,3)],           # Left end (row 1, cols 0-3, 4 frames)
#              "left_mid":[(1,4),(1,5),(1,6),(1,7)],           # Left mid (row 1, cols 4-7, 4 frames)
#              "right_end":[(2,0),(2,1),(2,2),(2,3)],          # Right end (row 2, cols 0-3, 4 frames)
#              "right_mid":[(2,4),(2,5),(2,6),(2,7)],          # Right mid (row 2, cols 4-7, 4 frames)
#              "up_end":[(3,0),(3,1),(3,2),(3,3)],             # Up end (row 3, cols 0-3, 4 frames)
#              "up_mid":[(3,4),(3,5),(3,6),(3,7)],             # Up mid (row 3, cols 4-7, 4 frames)
#              "down_end":[(4,0),(4,1),(4,2),(4,3)],           # Down end (row 4, cols 0-3, 4 frames)
#              "down_mid":[(4,4),(4,5),(4,6),(4,7)],           # Down mid (row 4, cols 4-7, 4 frames)
#             }

# ACTUAL SPRITE SHEET (all frames in row 0):
# [Centre][Centre][Centre][Centre][LeftExt][LeftExt][RightExt][RightExt][UpExt][UpExt][DownExt][DownExt]
# Col:  0      1       2       3        4         5         6          7         8      9      10       11

# EXPLOSION = {"centre":[(0,0),(0,1),(0,2),(0,3)],              # Center cross: row 0, cols 0-3 (4 animation frames)
#              "left_end":[(0,4),(0,4),(0,4),(0,4)],            # Left arm end: row 0, col 4 (static, repeated for 4 frames)
#              "left_mid":[(0,5),(0,5),(0,5),(0,5)],            # Left arm mid: row 0, col 5 (static, repeated for 4 frames)
#              "right_end":[(0,6),(0,6),(0,6),(0,6)],           # Right arm end: row 0, col 6 (static, repeated for 4 frames)
#              "right_mid":[(0,7),(0,7),(0,7),(0,7)],           # Right arm mid: row 0, col 7 (static, repeated for 4 frames)
#              "up_end":[(0,8),(0,8),(0,8),(0,8)],              # Up arm end: row 0, col 8 (static, repeated for 4 frames)
#              "up_mid":[(0,9),(0,9),(0,9),(0,9)],              # Up arm mid: row 0, col 9 (static, repeated for 4 frames)
#              "down_end":[(0,10),(0,10),(0,10),(0,10)],        # Down arm end: row 0, col 10 (static, repeated for 4 frames)
#              "down_mid":[(0,11),(0,11),(0,11),(0,11)],        # Down arm mid: row 0, col 11 (static, repeated for 4 frames)
#             }
# EXPLOSION = {"centre":[(2,7),(2,8),(2,9),(2,10)],
#              "left_end":[(3,0),(3,1),(3,2),(3,3)],
#              "right_end":[(3,0),(3,1),(3,2),(3,3)],
#              "up_end":[(4,0),(4,1),(4,2),(4,3)],
#              "down_end":[(4,0),(4,1),(4,2),(4,3)],
#              "left_mid":[(3,4),(3,5),(3,6),(3,7)], 
#              "right_mid":[(3,4),(3,5),(3,6),(3,7)],
#              "up_mid":[(4,4),(4,5),(4,6),(4,7)],
#              "down_mid":[(4,4),(4,5),(4,6),(4,7)],
#             }


#BOMB = {"bomb": [(0,2)]}  #bomb animation frames

# EXPLOSION = {"centre":[(0,0),(0,1),(0,2),(0,1)],
#              "horz":[(1,0),(1,1),(1,2),(1,1)],
#              "vert":[(2,0),(2,1),(2,2),(2,1)],
#              "end_up":[(3,0),(3,1),(3,2),(3,1)],
#              "end_down":[(4,0),(4,1),(4,2),(4,1)],
#              "end_left":[(5,0),(5,1),(5,2),(5,1)],
#              "end_right":[(6,0),(6,1),(6,2),(6,1)],
#            }