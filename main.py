# ============================================================================
# FILE: main.py - ENTRY POINT OF BOMBERMAN GAME
# ============================================================================
# PURPOSE:
#   Initializes and runs the main Bomberman game loop. Handles:
#   - Window creation and management (resizable, fullscreen toggle)
#   - Event processing (input, window resize, fullscreen toggle with F11)
#   - Game state updates and rendering
#
# DEPENDENCIES:
#   - pygame: Core game engine
#   - Assets: Loads and manages sprites, images, and game resources
#   - Game: Core game logic (player, blocks, level management)
#   - gamesetting: Global game configuration and constants
#   - home: Home menu interface
# ============================================================================

import pygame
from assets import Assets  # Class to manage all game assets (images, sounds, sprites)
from game import Game      # Core game logic (levels, players, blocks, camera)
import gamesetting as gs   # Global settings (screen size, FPS, colors, tile sizes, etc.)
import home                # Home menu module

# ============================================================================
# CLASS: Bomberman - Main game controller and window manager
# ============================================================================
class Bomberman:
  def __init__(self, screen):
    """
    CONSTRUCTOR - Initialize the Bomberman game window and core systems
    
    PARAMETERS:
    - screen: pygame.Surface - The existing screen/window to use
    
    STEPS:
    1. Use the provided screen instead of creating a new one
    2. Store windowed size for fullscreen toggle restoration
    3. Load game assets (sprites, images)
    4. Create the Game object (handles logic, camera, level)
    5. Initialize frame rate clock for consistent 60 FPS
    6. Set running flag to control main loop
    """
    # Use the existing screen passed from home menu
    self.screen = screen
    
    # Get current screen size
    self.windowed_size = (self.screen.get_width(), self.screen.get_height())
    self.fullscreen = False

    # Update window title for game
    pygame.display.set_caption("Bomba~ Na! - Game")
    
    # Create an instance of the Assets class to load and manage all game resources
    self.ASSETS = Assets()
    
    # Create the main Game object
    self.GAME = Game(self, self.ASSETS)
    
    # Create a Clock object to manage the game's frame rate (FPS)
    self.FPS = pygame.time.Clock()

    self.running = True

  def input(self):
    """
    INPUT HANDLER - Process all user input events and window events
    
    RESPONSIBILITIES:
    - Poll pygame events (keyboard, mouse, window events)
    - Handle ESC key to exit game
    - Handle F11 to toggle fullscreen mode
    - Handle window resize events (VIDEORESIZE)
    - Forward event list to Game and Character for their processing
    
    KEY EVENTS HANDLED:
    1. QUIT: Exit the game when user closes the window
    2. KEYDOWN + ESCAPE: Exit the game when user presses ESC
    3. KEYDOWN + F11: Toggle between fullscreen and windowed modes
       - On fullscreen: hides taskbar, hides mouse cursor
       - On windowed: shows cursor, restores previous window size
    4. VIDEORESIZE: User resizes the window
       - Clamps new size to display resolution
       - Updates stored windowed size for later restoration
    """
    # Poll events centrally so we can handle window resize and forward events
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.running = False
        elif event.key == pygame.K_F11:
          # Toggle fullscreen mode
          info = pygame.display.Info()
          if not self.fullscreen:
            # Enter exclusive fullscreen at current display resolution
            self.fullscreen = True
            # Save the last windowed size before switching
            try:
              self.windowed_size = (self.screen.get_width(), self.screen.get_height())
            except Exception:
              pass
            flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), flags)
            pygame.mouse.set_visible(False)
          else:
            # Restore previous windowed size and make resizable again
            self.fullscreen = False
            w, h = self.windowed_size
            self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
            pygame.mouse.set_visible(True)
      elif event.type == pygame.VIDEORESIZE:
        # Clamp resize to the current display resolution
        info = pygame.display.Info()
        new_w = min(event.w, info.current_w)
        new_h = min(event.h, info.current_h)
        # Only update the stored windowed size when not fullscreen
        self.screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
        if not getattr(self, 'fullscreen', False):
          self.windowed_size = (new_w, new_h)

    # Pass the event list to the Game so it can forward to the Character, etc.
    self.GAME.input(events)
        
  def update(self):
    """
    UPDATE - Advance game state and timing
    
    RESPONSIBILITIES:
    1. Control frame rate to maintain consistent 60 FPS
    2. Delegate game state updates to Game object
       - This includes sprite updates, player movement, camera interpolation
    
    PARAMETERS:
    - None (operates on internal state)
    
    NOTES:
    - Called once per game loop iteration
    - Camera lerp/smoothing happens inside Game.update()
    """
    # Control the frame rate to a constant value defined in gamesetting (gs.FPS)
    # This makes the game run at the same speed regardless of the computer's performance.
    self.FPS.tick(gs.FPS)
    # Also update the Game logic (handles smoothing camera interpolation)
    self.GAME.update()

  # Method for drawing all game elements to the screen
  def draw(self, window):
    """
    DRAW - Render all game visuals to the screen
    
    RENDERING PIPELINE:
    1. Fill screen with black background (gs.BLACK)
    2. Delegate drawing to Game object
       - Game draws background tiles, blocks, sprites with camera offsets applied
    3. Update the display buffer to show the rendered frame
    
    PARAMETERS:
    - window: pygame.Surface representing the main screen
    
    NOTES:
    - Called once per game loop iteration after update()
    - All camera offset calculations are handled inside Game.draw()
    """
    # window.blit(self.ASSETS.sprite_sheet,(0,0))
    self.GAME.draw(window) # Delegate drawing of game world, sprites, and camera-adjusted visuals
    pygame.display.update() # Swap buffers and display the rendered frame

  # The main game loop method
  def rungame(self):
    """
    MAIN GAME LOOP - Core loop that runs until game exits
    
    LOOP SEQUENCE (runs every frame):
    1. input() - Process all user input and window events
    2. update() - Update game state and advance frame timer
    3. draw(screen) - Render all visuals to the screen buffer
    
    The loop continues as long as self.running is True.
    When user closes window or presses ESC, running is set to False and loop exits.
    """
    while self.running == True:
      self.input()           # 1. Handle user input and window events
      self.update()          # 2. Update game state (position, logic, timing)
      self.draw(self.screen) # 3. Render all game visuals


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
# Standard Python convention: this block ensures the game only runs when 
# the script is executed directly (not imported as a module)
if __name__ == "__main__":
  # Initialize pygame
  pygame.init()
  
  # Create the main window
  info = pygame.display.Info()
  screen_w = min(gs.SCREENWIDTH, info.current_w)
  screen_h = min(gs.SCREENHEIGHT, info.current_h)
  screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
  pygame.display.set_caption("Bomba~ Na!")
  
  # Show home menu first
  should_start = home.run_menu(screen)
  
  # If user clicked start, run the game
  if should_start:
    game = Bomberman(screen)
    game.rungame()
  
  # Clean up when done
  pygame.quit()