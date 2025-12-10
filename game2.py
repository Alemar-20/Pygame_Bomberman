import pygame

def run_game():
    pygame.init()

    screen = pygame.display.set_mode((1300, 700))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 120, 200))   # Your game logic here
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()