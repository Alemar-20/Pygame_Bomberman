import pygame

pygame.init()

# Window size
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Empty Window")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background color (optional)
    screen.fill((255, 255, 255))

    pygame.display.update()

pygame.quit()