import pygame
from assets import Assets # Class to manage all game assets (images, sounds, etc.)
from game import Game # Class that handles the main game logic (levels, players, enemies)
import gamesetting as gs # Module/file containing global game settings (screen size, FPS, colors,Sprite Sizes(width/height),etc)

# This is main.py - the entry point of the Bomberman game.

class Bomberman:
  def __init__(self):
    pygame.init()

    # 2. Set up the display window (the 'screen')
    #    It uses screen dimensions defined in the gamesetting module (gs)
    self.screen = pygame.display.set_mode((gs.SCREENWIDTH, gs.SCREENHEIGHT))

    # 3. Set the title
    pygame.display.set_caption("Bomba~ Na!")



    # 4. Create an instance of the Assets class to load and manage all game resources
    self.ASSETS = Assets()
    # 5. Create the main Game object
    #    It passes 'self' (the main Bomberman indstance) and the Assets object for the Game class to use
    self.GAME = Game(self, self.ASSETS)
    # 6. Create a Clock object to manage the game's frame rate (FPS)
    self.FPS = pygame.time.Clock()

    self.running = True

  # Method for handling all user input (keyboard, mouse, window events)
  def input(self):

    # Delegate input handling to the specific Game object (e.g., player movement, bomb dropping)
    self.GAME.input()
        
  # Method for updating the game state (movement, physics, collision checks, enemy AI)
  def update(self):
    # Control the frame rate to a constant value defined in gamesetting (gs.FPS)
    # This makes the game run at the same speed regardless of the computer's performance.
    self.FPS.tick(gs.FPS)

  # Method for drawing all game elements to the screen
  def draw(self,window):
    window.fill(gs.BLACK) # 1. Fill the window surface with a background color (BLACK defined in gs)
    # window.blit(self.ASSETS.sprite_sheet,(0,0))
    self.GAME.draw(window) # 3. Delegate the actual drawing of players, bombs, and maps to the Game object
    pygame.display.update() #4. Update the full screen to display what was just drawn

  # The main game loop method
  def rungame(self):
    while self.running == True:
      self.input() # 1. Handle user input
      self.update() # 2. Update the game state (position/logic)
      self.draw(self.screen)# 3. Redraw the screen (pass the main screen surface to the draw method)


# Standard Python convention: this block ensures the game only runs when the script is executed directly
if __name__ == "__main__":
  game = Bomberman() # 1. Create an instance of the Bomberman game
  game.rungame() # 2. Start the main game loop
  pygame.quit() #3. Once the 'rungame' loop exits (if 'self.running' is set to False), 
    #    this cleans up all Pygame resources and safely closes the application.