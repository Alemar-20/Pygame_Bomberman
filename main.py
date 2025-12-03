import pygame
from assets import Assets # Class to manage all game assets (images, sounds, etc.)
from game import Game # Class that handles the main game logic (levels, players, enemies)
import gamesetting as gs # Module/file containing global game settings (screen size, FPS, colors,Sprite Sizes(width/height),etc)

# This is main.py - the entry point of the Bomberman game.

class Bomberman:
  def __init__(self):
    pygame.init()
    # 2. Set up the display window (the 'screen')
    #    Use the configured size but clamp to the current display so it fits on any device.
    info = pygame.display.Info()
    screen_w = min(gs.SCREENWIDTH, info.current_w)
    screen_h = min(gs.SCREENHEIGHT, info.current_h)
    # Create a resizable window so players can adjust size at runtime
    self.screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)

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
    # Poll events centrally so we can handle window resize and forward events
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.running = False
      elif event.type == pygame.VIDEORESIZE:
        # Clamp resize to the current display resolution
        info = pygame.display.Info()
        new_w = min(event.w, info.current_w)
        new_h = min(event.h, info.current_h)
        self.screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)

    # Pass the event list to the Game so it can forward to the Character, etc.
    self.GAME.input(events)
        
  # Method for updating the game state (movement, physics, collision checks, enemy AI)
  def update(self):
    # Control the frame rate to a constant value defined in gamesetting (gs.FPS)
    # This makes the game run at the same speed regardless of the computer's performance.
    self.FPS.tick(gs.FPS)
    # Also update the Game logic (handles smoothing camera interpolation)
    self.GAME.update()

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