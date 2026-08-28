import pygame

pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("Pathfinder")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((14, 31, 61))
    pygame.display.flip()

pygame.quit()
