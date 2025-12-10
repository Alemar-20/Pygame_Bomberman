#This is gamesetting.py - contains global settings for the Bomberman game

# A common, game-friendly default resolution that fits most laptops nicely
SCREENWIDTH = 1280
SCREENHEIGHT = 720  #default 720
               #892

# GAME FRAMES PER SECONDS
FPS = 60

# Y COORDINATE OFFSET FOR SPRITES
Y_OFFSET = 92

# Enemy Attributes
ENEMIES = {"ballom" : {"speed": 1, "wall_hack":False, "chase_player": False, "LoS": 0, "see_player_hack": False},
           "onil": {"speed": 2, "wall_hack":False, "chase_player": True, "LoS": 4, "see_player_hack": False},
           "dahl": {"speed": 2, "wall_hack":False, "chase_player": True, "LoS": 0, "see_player_hack": False},
           "minvo": {"speed": 2, "wall_hack":False, "chase_player": True, "LoS": 4, "see_player_hack": True},
           "doria": {"speed": 0.5, "wall_hack":True, "chase_player": True, "LoS": 6, "see_player_hack": True},
           "ovape": {"speed": 1, "wall_hack":True, "chase_player": True, "LoS": 8, "see_player_hack": False},
           "pass": {"speed": 2, "wall_hack":True, "chase_player": True, "LoS": 12, "see_player_hack": False},
           "pontan": {"speed": 4, "wall_hack":True, "chase_player": True, "LoS": 30, "see_player_hack": False}}
            
# ACTUAL SPRITE SIZE FROM YOUR SHEET
SPRITE_WIDTH = 32   # Most common size for this styles
SPRITE_HEIGHT = 32

# TILE SIZE FROM YOUR TILE SHEET
TILE_WIDTH = 32
TILE_HEIGHT = 32

# GAME MATRIX 
SIZE = 64  # SIZE OF EACH TILE IN PIXELS
# Increase the level size so the world is larger than the screen
# This allows the camera to scroll when the player moves around
ROWS = 20 #def 20
COLS = 30 # 40

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
    "idle_down": [(0, 0)],
    "idle_left": [(3, 0)],
    "idle_right": [(1, 0)],
    "idle_up": [(2, 0)],
    
    # Row 1: Dead/Vulnerable (Adjusting based on observation)
    "dead_anim": [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),(4,7),(4,8)], 
    
    # Row 3: Bomb/Kick Animation (Example)
    "kick_anim": [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)],
    
    # Row 4: Happy/Win
    "win_anim": [(6, 0), (6, 1), (6, 2), (6, 3),(6,4),(6,5),(6,7)],
    
    # Row 5: Sleep
    "sleep_anim": [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4),(7,5),(7,6),(7,7)],
}

HARD_BLOCK = {"hard_block":[(2,1)]} #0,1 default  #0,4
SOFT_BLOCK = {"soft_block":[(0,0),(0,1),(0,2),(0,3),
                            (1,0),(1,2),(1,3),(1,4),
                            (2,0),(2,1),(2,2)]} #block for purple soft block [(0,7]}
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
BALLOM = {"walk_right":[(5,0),(5,1),(5,2)],
          "walk_down":[(5,0),(5,1),(5,2)],
          "walk_left":[(5,3),(5,4),(5,5)],
          "walk_up":[(5,3),(5,4),(5,5)],
          "death":[(5,6),(5,7),(5,8),(5,9),(5,10)],}


ONIL = {"walk_right":[(8,0),(8,1),(8,2)],
        "walk_down":[(8,0),(8,1),(8,2)],
        "walk_left":[(8,3),(8,4),(8,5)],
        "walk_up":[(8,3),(8,4),(8,5)],
        "death":[(8,6),(8,7),(8,8),(8,9),(8,10)],
        }
DAHL = {"walk_right":[(10,0),(10,1),(10,2)],
        "walk_down":[(10,0),(10,1),(10,2)],
        "walk_left":[(10,3),(10,4),(10,5)],
        "walk_up":[(10,3),(10,4),(10,5)],
        "death":[(10,6),(10,7),(10,8),(10,9),(10,10)],
        }
MINVO = {"walk_right":[(6,0),(6,1),(6,2)],
        "walk_down":[(6,0),(6,1),(6,2)],
        "walk_left":[(6,3),(6,4),(6,5)],
        "walk_up":[(6,3),(6,4),(6,5)],
        "death":[(6,6),(6,7),(6,8),(6,9),(6,10)],
        }
DORIA = {"walk_right":[(9,0),(9,1),(9,2)],
        "walk_down":[(9,0),(9,1),(9,2)],
        "walk_left":[(9,3),(9,4),(9,5)],
        "walk_up":[(9,3),(9,4),(9,5)],
        "death":[(9,6),(9,7),(9,8),(9,9),(9,10)],
        }
OVAPE = {"walk_right":[(11,0),(11,1),(11,2)],
        "walk_down":[(11,0),(11,1),(11,2)],
        "walk_left":[(11,3),(11,4),(11,5)],
        "walk_up":[(11,3),(11,4),(11,5)],
        "death":[(11,6),(11,7),(11,8),(11,9),(11,10)],
        }
PASS = {"walk_right":[(7,0),(7,1),(7,2)],
        "walk_down":[(7,0),(7,1),(7,2)],
        "walk_left":[(7,3),(7,4),(7,5)],
        "walk_up":[(7,3),(7,4),(7,5)],
        "death":[(7,6),(7,7),(7,8),(7,9),(7,10)],
        }
PONTAN = {"walk_right":[(5,11),(6,11),(7,11),(8,11)],
        "walk_down":[(5,11),(6,11),(7,11),(8,11)],
        "walk_left":[(5,11),(6,11),(7,11),(8,11)],
        "walk_up":[(5,11),(6,11),(7,11),(8,11)],
        "death":[(9,11),(5,7),(5,8),(5,9),(5,10)],
        }