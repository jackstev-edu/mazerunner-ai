import pygame

pygame.init()  # boots pygame's internals; must run before anything else
screen = pygame.display.set_mode((800, 480))  # returns the window surface we'll draw onto
pygame.display.set_caption("Pathfinder")

COLS, ROWS, CELL_SIZE = 25, 15, 32  # 25*32=800, 15*32=480 = grid tiles 

running = True
while running:
    for event in pygame.event.get():        # all events since last frame, as one list
        if event.type == pygame.QUIT:       # fires only on the window's X button
            running = False                 # loop exits cleanly on its next check, not mid-frame

    screen.fill((14, 31, 61))  # must run before the grid loop, since draws layer on top

    for row in range(ROWS):                  # advances one row at a time
        for col in range(COLS):              # nested loop hits all 375 cells exactly once
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # grid index -> pixel position
            pygame.draw.rect(screen, (24, 51, 97), rect)             # filled cell, drawn before the outline
            pygame.draw.rect(screen, (42, 82, 136), rect, width=1)   # width=1 -> outline only

    pygame.display.flip()  # swaps the off-screen buffer onto the actual display

pygame.quit()  # releases pygame's resources on exit