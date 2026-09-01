# main.py
# pygame setup, the event loop, and animation timing, ties grid_state
# and ui together into the actual running app.

import pygame
from pathfinding import bfs, dijkstra, astar # all three pathfinding algorithms from pathfinding.py
import time                                    # for timing how long each search takes
import grid_state
from grid_state import COLS, ROWS, CELL_SIZE, apply_tool, cell_at_pixel
import ui   # module-level import, referenced as ui.X

pygame.init()  # boots pygame's internals; must run before anything else

screen = pygame.display.set_mode((COLS * CELL_SIZE, ui.GRID_HEIGHT + ui.UI_HEIGHT))  # fixed size, back to original
pygame.display.set_caption("Maze Runner")
clock = pygame.time.Clock()  # tracks real time between frames, used to pace the animation

font = pygame.font.SysFont("couriernew", 18, bold=True)          # button labels, bold and bigger for legibility
heading_font = pygame.font.SysFont("couriernew", 14, bold=True)  # section headings, bold
small_font = pygame.font.SysFont("couriernew", 14)                 # blurbs and status text, bigger but not bold

painting = False # enables painting when mouse click is held
algorithm = "bfs" # default pathfinding algorithm
path = None # Initially no path exists
explored_order = [] # Initially no exploration order exists
reveal_index = 0 # Index to reveal explored cells one by one
path_reveal_index = 0 # Index to reveal path cells one by one
animating = False # Flag to indicate if animation is in progress
REVEAL_DELAY_MS = 25       # milliseconds between each explored cell reveal, lower is faster
PATH_REVEAL_DELAY_MS = 60  # slower than exploration, so the final path reads clearly
reveal_timer = 0           # counts down to the next explored cell reveal
path_reveal_timer = 0      # counts down to the next path cell reveal
status_message = "Draw a maze, then click Run."  # shown in the UI panel, updates after every search
status_color = (143, 166, 204)                     # neutral dim color until a search actually runs

# Function to run the selected pathfinding algorithm and update the path and explored order
def run_search():
    global path, explored_order, reveal_index, path_reveal_index, animating, status_message, status_color, reveal_timer, path_reveal_timer
    started = time.perf_counter()                      # timestamp before the algorithm runs
    if algorithm == "bfs":
        path, explored_order = bfs(grid_state.start, grid_state.end, grid_state.walls, ROWS, COLS)
    elif algorithm == "dijkstra":
        path, explored_order = dijkstra(grid_state.start, grid_state.end, grid_state.walls, grid_state.mud, ROWS, COLS)
    elif algorithm == "astar":
        path, explored_order = astar(grid_state.start, grid_state.end, grid_state.walls, grid_state.mud, ROWS, COLS)
    elapsed_ms = (time.perf_counter() - started) * 1000   # seconds to milliseconds, easier to read

    reveal_index = 0
    path_reveal_index = 0
    reveal_timer = 0     # start revealing immediately, not after one full delay
    path_reveal_timer = 0
    animating = True

    if path is None:
        status_message = "No path found, maze is fully blocked"
        status_color = (240, 96, 61)                        # coral, signals failure
    else:
        cost = sum(5 if cell in grid_state.mud else 1 for cell in path[1:])   # real cost, not just step count
        status_message = f"Path found: {len(path) - 1} steps, cost {cost}, {len(explored_order)} nodes explored, {elapsed_ms:.1f}ms"
        status_color = (95, 212, 232)                        # cyan, signals success

# Main loop - runs until the user closes the window
running = True
while running:
    dt = clock.tick(60)  # milliseconds since the last frame, also caps the frame rate at 60fps

    for event in pygame.event.get():        # all events since last frame, as one list
        if event.type == pygame.QUIT:       # fires only on the window's X button
            running = False                 # loop exits cleanly on its next check, not mid-frame
        elif event.type == pygame.MOUSEBUTTONDOWN: # Triggers when mouse click is pressed
            clicked_button = False
            # Check if any tool button was clicked
            for b in ui.TOOL_BUTTONS:
                if b["rect"].collidepoint(event.pos):
                    grid_state.tool = b["tool"]     # no global needed, mutating the module, not a local name
                    clicked_button = True
            # Check if Start or End was clicked
            for b in ui.ACTION_BUTTONS:
                if b["rect"].collidepoint(event.pos):
                    grid_state.tool = b["tool"]
                    clicked_button = True
            # Check if any algorithm button was clicked
            for b in ui.ALGO_BUTTONS:
                if b["rect"].collidepoint(event.pos):
                    algorithm = b["algo"]
                    clicked_button = True
            # Check if the run button was clicked
            if ui.RUN_BUTTON.collidepoint(event.pos):
                run_search()
                clicked_button = True
            # If no button was clicked, check if the click was on the grid to start painting
            if not clicked_button and event.pos[1] < ui.GRID_HEIGHT:   # only paint if the click actually hit the grid
                painting = True
                apply_tool(cell_at_pixel(event.pos))
        elif event.type == pygame.MOUSEBUTTONUP: # Triggers when mouse click is released
            painting = False # disable painting when mouse click is released
        elif event.type == pygame.MOUSEMOTION: # Mouse motion monitors user movement while mouse click is held down
            if painting: # Guard for mouse motion events, only apply tool if mouse click is held
                apply_tool(cell_at_pixel(event.pos)) 

    if animating:  # If animation is in progress, count down to the next reveal
        if reveal_index < len(explored_order):
            reveal_timer -= dt
            if reveal_timer <= 0:
                reveal_index += 1
                reveal_timer = REVEAL_DELAY_MS
        elif path and path_reveal_index < len(path):
            path_reveal_timer -= dt
            if path_reveal_timer <= 0:
                path_reveal_index += 1
                path_reveal_timer = PATH_REVEAL_DELAY_MS
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

    ui.draw_panel_background(screen)

    mouse_pos = pygame.mouse.get_pos()   # checked once per frame, reused for every button's hover check

    ui.draw_heading(screen, heading_font, "Tools", ui.TOOLS_HEADING_Y)
    for b in ui.TOOL_BUTTONS:
        hovering = b["rect"].collidepoint(mouse_pos)
        ui.draw_button(screen, font, b["rect"], b["label"], grid_state.tool == b["tool"], hovering)
    ui.draw_blurb(screen, small_font, ui.get_blurb(ui.TOOL_BUTTONS, "tool", grid_state.tool), ui.TOOLS_BLURB_Y)

    ui.draw_heading(screen, heading_font, "Pathfinding Algorithms", ui.ALGO_HEADING_Y)
    for b in ui.ALGO_BUTTONS:
        hovering = b["rect"].collidepoint(mouse_pos)
        ui.draw_button(screen, font, b["rect"], b["label"], algorithm == b["algo"], hovering)
    ui.draw_blurb(screen, small_font, ui.get_blurb(ui.ALGO_BUTTONS, "algo", algorithm), ui.ALGO_BLURB_Y)

    for b in ui.ACTION_BUTTONS:
        hovering = b["rect"].collidepoint(mouse_pos)
        ui.draw_button(screen, font, b["rect"], b["label"], grid_state.tool == b["tool"], hovering)
    ui.draw_run_button(screen, font, ui.RUN_BUTTON, ui.RUN_BUTTON.collidepoint(mouse_pos))

    ui.draw_status(screen, small_font, status_message, status_color)

    pygame.display.flip()  # swaps the off-screen buffer onto the actual display

pygame.quit()  # releases pygame's resources on exit