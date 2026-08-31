import pygame
from pathfinding import bfs, dijkstra, astar # all three pathfinding algorithms from pathfinding.py

pygame.init()  # boots pygame's internals; must run before anything else
screen = pygame.display.set_mode((800, 480))  # returns the window surface we'll draw onto
pygame.display.set_caption("Maze Runner")

COLS, ROWS, CELL_SIZE = 25, 15, 32  # 25*32=800, 15*32=480 = grid tiles

# Initialization of user interfacing maze elements
walls = set()  # empty set of wall coordinates, to be filled later
mud = set()  # empty set of mud coordinates, to be filled later
start = (2,2) # Maze starting point
end = (ROWS-3, COLS-3) #
tool = "wall" # current tool selected for painting
painting = False # enables painting when mouse click is held
algorithm = "bfs" # default pathfinding algorithm

# translating pixel coordinates to grid coordinates
def cell_at_pixel(pos): 
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

# Function to apply one tool at a time to a cell, based on the current tool selected
def apply_tool(cell):
    global start, end  # Updating preinitialized start and end points - hence "global"
    if tool == "wall":
        mud.discard(cell)  # Discard obstabcle before overriding with wall
        walls.symmetric_difference_update({cell})
    elif tool == "mud":
        walls.discard(cell)  # Discard obstabcle before overriding with mud
        mud.symmetric_difference_update({cell})
    elif tool == "erase": # Indiscriminate removal of any obstacles from the cell
        walls.discard(cell)
        mud.discard(cell)
    elif tool == "start": # Update start point to clicked cell
        start = cell
    elif tool == "end": # Update end point to clicked cell
        end = cell

# Main loop - runs until the user closes the window
running = True
while running:
    for event in pygame.event.get():        # all events since last frame, as one list
        if event.type == pygame.QUIT:       # fires only on the window's X button
            running = False                 # loop exits cleanly on its next check, not mid-frame
        elif event.type == pygame.MOUSEBUTTONDOWN:
            painting = True # enable painting when mouse click is held
            apply_tool(cell_at_pixel(event.pos)) # apply tool to cell at mouse click position
        elif event.type == pygame.MOUSEBUTTONUP: # Triggers when mouse click is released
            painting = False # disable painting when mouse click is released
        elif event.type == pygame.MOUSEMOTION: # Mouse motion monitors user movement while mouse click is held down
            if painting: # Guard for mouse motion events, only apply tool if mouse click is held
                apply_tool(cell_at_pixel(event.pos)) 
        elif event.type == pygame.KEYDOWN: # keyboard events for tool selection
            if event.key == pygame.K_w: # wall tool
                tool = "wall"
            elif event.key == pygame.K_m: # mud tool
                tool = "mud"
            elif event.key == pygame.K_x: # erase tool
                tool = "erase"
            elif event.key == pygame.K_s: # start point tool
                tool = "start"
            elif event.key == pygame.K_e:  # end point tool
                tool = "end"
            elif event.key == pygame.K_1: # select BFS algorithm
                algorithm = "bfs"
            elif event.key == pygame.K_2: # select Dijkstra's algorithm
                algorithm = "dijkstra"  
            elif event.key == pygame.K_3:  # select A* algorithm
                algorithm = "astar"
            elif event.key == pygame.K_SPACE:
                if algorithm == "bfs":
                    path = bfs(start, end, walls, ROWS, COLS)
                elif algorithm == "dijkstra":
                    path = dijkstra(start, end, walls, mud, ROWS, COLS)
                elif algorithm == "astar":
                    path = astar(start, end, walls, mud, ROWS, COLS)
                print(path)  # still temporary -- we'll draw this instead of printing it next
                


    screen.fill((14, 31, 61))  # must run before the grid loop, since draws layer on top

# Draw grid and cells based on current state
    for row in range(ROWS):                  
        for col in range(COLS):              # nested loop hits all 375 cells exactly once
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # grid index -> pixel position
            color = (8, 18, 42) if (row, col) in walls else (185, 128, 63) if (row, col) in mud else (24, 51, 97) #Cell colour now dependent on state
            pygame.draw.rect(screen, color, rect)  # updated to use the correct color input
            pygame.draw.rect(screen, (42, 82, 136), rect, width=1)   # width=1 - outline only

    # Creating start and end point icons
    start_center = (start[1] * CELL_SIZE + CELL_SIZE // 2, start[0] * CELL_SIZE + CELL_SIZE // 2)
    end_center = (end[1] * CELL_SIZE + CELL_SIZE // 2, end[0] * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, (242, 184, 75), start_center, CELL_SIZE // 3)  # amber start marker
    pygame.draw.circle(screen, (240, 96, 61), end_center, CELL_SIZE // 3)     # coral end marker

    pygame.display.flip()  # swaps the off-screen buffer onto the actual display

pygame.quit()  # releases pygame's resources on exit