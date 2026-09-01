# main.py
# pygame setup, the event loop, and animation timing -- ties grid_state
# and ui together into the actual running app.

import pygame
from pathfinding import bfs, dijkstra, astar # all three pathfinding algorithms from pathfinding.py
import grid_state
from grid_state import COLS, ROWS, CELL_SIZE, apply_tool, cell_at_pixel
from ui import GRID_HEIGHT, UI_HEIGHT, TOOL_BUTTONS, ALGO_BUTTONS, RUN_BUTTON, draw_button

pygame.init()  # boots pygame's internals; must run before anything else

screen = pygame.display.set_mode((COLS * CELL_SIZE, GRID_HEIGHT + UI_HEIGHT))  # fixed: now tall enough for the buttons
pygame.display.set_caption("Maze Runner")
font = pygame.font.SysFont("couriernew", 16) # Renders button labels

painting = False # enables painting when mouse click is held
algorithm = "bfs" # default pathfinding algorithm
path = None # Initially no path exists
explored_order = [] # Initially no exploration order exists
reveal_index = 0 # Index to reveal explored cells one by one
path_reveal_index = 0 # Index to reveal path cells one by one
animating = False # Flag to indicate if animation is in progress

# Function to run the selected pathfinding algorithm and update the path and explored order
def run_search():
    global path, explored_order, reveal_index, path_reveal_index, animating   # this function reassigns all five
    if algorithm == "bfs":
        path, explored_order = bfs(grid_state.start, grid_state.end, grid_state.walls, ROWS, COLS)
    elif algorithm == "dijkstra":
        path, explored_order = dijkstra(grid_state.start, grid_state.end, grid_state.walls, grid_state.mud, ROWS, COLS)
    elif algorithm == "astar":
        path, explored_order = astar(grid_state.start, grid_state.end, grid_state.walls, grid_state.mud, ROWS, COLS)
    reveal_index = 0
    path_reveal_index = 0
    animating = True
    if path is None:
        print("No path found -- maze is fully blocked")

# Main loop - runs until the user closes the window
running = True
while running:
    for event in pygame.event.get():        # all events since last frame, as one list
        if event.type == pygame.QUIT:       # fires only on the window's X button
            running = False                 # loop exits cleanly on its next check, not mid-frame
        elif event.type == pygame.MOUSEBUTTONDOWN: # Triggers when mouse click is pressed
            clicked_button = False
            # Check if any tool or algorithm button was clicked
            for b in TOOL_BUTTONS:
                if b["rect"].collidepoint(event.pos):
                    grid_state.tool = b["tool"]     # no `global` needed -- mutating the module, not a local name
                    clicked_button = True
            # Check if any algorithm button was clicked
            for b in ALGO_BUTTONS:
                if b["rect"].collidepoint(event.pos):
                    algorithm = b["algo"]
                    clicked_button = True
            # Check if the run button was clicked
            if RUN_BUTTON.collidepoint(event.pos):
                run_search()
                clicked_button = True
            # If no button was clicked, check if the click was on the grid to start painting
            if not clicked_button and event.pos[1] < GRID_HEIGHT:   # only paint if the click actually hit the grid
                painting = True
                apply_tool(cell_at_pixel(event.pos))
        elif event.type == pygame.MOUSEBUTTONUP: # Triggers when mouse click is released
            painting = False # disable painting when mouse click is released
        elif event.type == pygame.MOUSEMOTION: # Mouse motion monitors user movement while mouse click is held down
            if painting: # Guard for mouse motion events, only apply tool if mouse click is held
                apply_tool(cell_at_pixel(event.pos)) 
        elif event.type == pygame.KEYDOWN: # keyboard events for tool selection
            if event.key == pygame.K_w: # wall tool
                grid_state.tool = "wall"
            elif event.key == pygame.K_m: # mud tool
                grid_state.tool = "mud"
            elif event.key == pygame.K_x: # erase tool
                grid_state.tool = "erase"
            elif event.key == pygame.K_s: # start point tool
                grid_state.tool = "start"
            elif event.key == pygame.K_e:  # end point tool
                grid_state.tool = "end"
            elif event.key == pygame.K_1: # select BFS algorithm
                algorithm = "bfs"
            elif event.key == pygame.K_2: # select Dijkstra's algorithm
                algorithm = "dijkstra"  
            elif event.key == pygame.K_3:  # select A* algorithm
                algorithm = "astar"
            elif event.key == pygame.K_SPACE: # run the selected pathfinding algorithm
                run_search()

    if animating:  # If animation is in progress, increment the reveal indices
        if reveal_index < len(explored_order):
            reveal_index = min(len(explored_order), reveal_index + max(1, len(explored_order) // 60)) # Increment reveal_index by a fraction of the total explored cells, but at least 1
        elif path and path_reveal_index < len(path):
            path_reveal_index = min(len(path), path_reveal_index + max(1, len(path) //30))  # Increment path_reveal_index by a fraction of the total path cells, but at least 1
        else:
            animating = False  # Stop animation when all cells are revealed

    screen.fill((14, 31, 61))  # must run before the grid loop, since draws layer on top

    # Color the grid based on the current state of walls, mud, explored cells, and empty cells
    explored_set = set(explored_order[:reveal_index])  # only what's been revealed so far this animation

    for row in range(ROWS):                  
        for col in range(COLS): # nested loop hits all 375 cells exactly once
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # grid index -> pixel position
            if (row, col) in grid_state.walls:
                color = (8, 18, 42) # dark blue marks the wall cells
            elif (row, col) in grid_state.mud:
                color = (185, 128, 63) # brown marks the mud cells
            elif (row, col) in explored_set:
                color = (95, 212, 232) # cyan marks the explored cells
            else:
                color = (24, 51, 97) # dark blue marks the empty cells
            pygame.draw.rect(screen, color, rect)  # updated to use the correct color input
            pygame.draw.rect(screen, (42, 82, 136), rect, width=1)

    # Creating start and end point icons
    start_center = (grid_state.start[1] * CELL_SIZE + CELL_SIZE // 2, grid_state.start[0] * CELL_SIZE + CELL_SIZE // 2)
    end_center = (grid_state.end[1] * CELL_SIZE + CELL_SIZE // 2, grid_state.end[0] * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, (242, 184, 75), start_center, CELL_SIZE // 3)  # amber start marker
    pygame.draw.circle(screen, (240, 96, 61), end_center, CELL_SIZE // 3)     # coral end marker

    if path_reveal_index > 1: # pygame.draw.lines requires at least 2 points to draw a line
        points = [(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2) for r, c in path[:path_reveal_index]] # convert grid coordinates to pixel coordinates
        pygame.draw.lines(screen, (242, 184, 75), False, points, width=4) # draw the path in amber color

    for b in TOOL_BUTTONS:
        draw_button(screen, font, b["rect"], b["label"], grid_state.tool == b["tool"])       # lit up when it's the active tool
    for b in ALGO_BUTTONS:
        draw_button(screen, font, b["rect"], b["label"], algorithm == b["algo"])  # lit up when it's the active algorithm
    draw_button(screen, font, RUN_BUTTON, "Run", False)    

    pygame.display.flip()  # swaps the off-screen buffer onto the actual display

pygame.quit()  # releases pygame's resources on exit