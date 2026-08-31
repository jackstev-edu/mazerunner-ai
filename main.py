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
end = (ROWS-3, COLS-3) # Maze ending point
tool = "wall" # current tool selected for painting
painting = False # enables painting when mouse click is held
algorithm = "bfs" # default pathfinding algorithm
path = None # Initially no path exists
explored_order = [] # Initially no exploration order exists
reveal_index = 0 # Index to reveal explored cells one by one
path_reveal_index = 0 # Index to reveal path cells one by one
animating = False # Flag to indicate if animation is in progress

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
            elif event.key == pygame.K_SPACE: # run the selected pathfinding algorithm
                if algorithm == "bfs":
                    path, explored_order = bfs(start, end, walls, ROWS, COLS)
                elif algorithm == "dijkstra":
                    path, explored_order = dijkstra(start, end, walls, mud, ROWS, COLS)
                elif algorithm == "astar":
                    path, explored_order = astar(start, end, walls, mud, ROWS, COLS)
                # restart the animation from scratch on every run
                reveal_index = 0          
                path_reveal_index = 0       
                animating = True
                if path is None:
                    print("No path found -- maze is fully blocked")
                

    if animating:  # If animation is in progress, increment the reveal indices
        if reveal_index < len(explored_order):
            reveal_index = min(len(explored_order), reveal_index + max(1, len(explored_order) // 60)) # Increment reveal_index by a fraction of the total explored cells, but at least 1
        elif path and path_reveal_index < len(path):
            path_reveal_index = min(len(path), path_reveal_index + max(1, len(path) //30))  # Increment path_reveal_index by a fraction of the total path cells, but at least 1
        else:
            animating = False  # Stop animation when all cells are revealed

    screen.fill((14, 31, 61))  # must run before the grid loop, since draws layer on top
    explored_set = set(explored_order[:reveal_index])  # Get the currently revealed explored cells

    # Draw grid and cells based on current state
    explored_set = set(explored_order[:reveal_index])  # only what's been revealed so far this animation

    # Color the grid based on the current state of walls, mud, explored cells, and empty cells
    for row in range(ROWS):                  
        for col in range(COLS): # nested loop hits all 375 cells exactly once
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # grid index -> pixel position
            if (row, col) in walls:
                color = (8, 18, 42) # dark blue marks the wall cells
            elif (row, col) in mud:
                color = (185, 128, 63) # brown marks the mud cells
            elif (row, col) in explored_set:
                color = (95, 212, 232) # cyan marks the explored cells
            else:
                color = (24, 51, 97) # dark blue marks the empty cells
            pygame.draw.rect(screen, color, rect)  # updated to use the correct color input
            pygame.draw.rect(screen, (42, 82, 136), rect, width=1)

    # Creating start and end point icons
    start_center = (start[1] * CELL_SIZE + CELL_SIZE // 2, start[0] * CELL_SIZE + CELL_SIZE // 2)
    end_center = (end[1] * CELL_SIZE + CELL_SIZE // 2, end[0] * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, (242, 184, 75), start_center, CELL_SIZE // 3)  # amber start marker
    pygame.draw.circle(screen, (240, 96, 61), end_center, CELL_SIZE // 3)     # coral end marker

    if path_reveal_index > 1: # pygame.draw.lines requires at least 2 points to draw a line
        points = [(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2) for r, c in path[:path_reveal_index]] # convert grid coordinates to pixel coordinates
        pygame.draw.lines(screen, (242, 184, 75), False, points, width=4) # draw the path in amber color

    pygame.display.flip()  # swaps the off-screen buffer onto the actual display

pygame.quit()  # releases pygame's resources on exit