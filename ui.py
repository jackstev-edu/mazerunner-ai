# ui.py
# Button layout and drawing for the on-screen toolbar. Takes whatever it
# needs (screen, font, which option is active) as arguments instead of
# reaching into grid_state or main directly -- keeps it reusable.

import pygame
from grid_state import ROWS, CELL_SIZE

GRID_HEIGHT = ROWS * CELL_SIZE # 480
UI_HEIGHT = 100 # height of the user interface area at the bottom of the screen

# Define the buttons for tools and algorithms, along with their positions and sizes
TOOL_BUTTONS = [
    {"label": "Wall",  "tool": "wall",  "rect": pygame.Rect(10, GRID_HEIGHT + 10, 80, 32)},
    {"label": "Mud",   "tool": "mud",   "rect": pygame.Rect(100, GRID_HEIGHT + 10, 80, 32)},
    {"label": "Erase", "tool": "erase", "rect": pygame.Rect(190, GRID_HEIGHT + 10, 80, 32)},
    {"label": "Start", "tool": "start", "rect": pygame.Rect(280, GRID_HEIGHT + 10, 80, 32)},
    {"label": "End",   "tool": "end",   "rect": pygame.Rect(370, GRID_HEIGHT + 10, 80, 32)},
]
ALGO_BUTTONS = [
    {"label": "BFS",      "algo": "bfs",      "rect": pygame.Rect(10, GRID_HEIGHT + 52, 80, 32)},
    {"label": "Dijkstra", "algo": "dijkstra", "rect": pygame.Rect(100, GRID_HEIGHT + 52, 100, 32)},
    {"label": "A*",       "algo": "astar",    "rect": pygame.Rect(210, GRID_HEIGHT + 52, 80, 32)},
]
RUN_BUTTON = pygame.Rect(300, GRID_HEIGHT + 52, 100, 32)

# Function to draw a button with a label and highlight it if it's active
def draw_button(screen, font, rect, label, active):
    color = (95, 212, 232) if active else (26, 55, 105)     # highlight whichever option is currently selected
    pygame.draw.rect(screen, color, rect, border_radius=4)
    text = font.render(label, True, (233, 239, 251))
    screen.blit(text, text.get_rect(center=rect.center))      # centers the label inside the button