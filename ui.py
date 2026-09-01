# ui.py
# Button layout and drawing for the on-screen toolbar. Takes whatever it
# needs (screen, font, which option is active) as arguments instead of
# reaching into grid_state or main directly, keeps it reusable.

import pygame
from grid_state import ROWS, CELL_SIZE

GRID_HEIGHT = ROWS * CELL_SIZE # 480
UI_HEIGHT = 130 # taller than before, room for a status/stats row below the buttons

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

def draw_panel_background(screen):
    panel_rect = pygame.Rect(0, GRID_HEIGHT, screen.get_width(), UI_HEIGHT)
    pygame.draw.rect(screen, (19, 42, 82), panel_rect)          # lighter navy, separates toolbar from grid
    pygame.draw.line(screen, (42, 82, 136), (0, GRID_HEIGHT), (screen.get_width(), GRID_HEIGHT), width=1)  # divider line

def draw_button(screen, font, rect, label, active, hover=False):
    if active:
        color = (95, 212, 232)              # cyan, currently selected
    elif hover:
        color = (35, 70, 130)                # lighter navy, cursor is over it but not clicked
    else:
        color = (26, 55, 105)                # default inactive navy
    pygame.draw.rect(screen, color, rect, border_radius=4)
    text = font.render(label, True, (233, 239, 251))
    screen.blit(text, text.get_rect(center=rect.center))      # centers the label inside the button

def draw_status(screen, font, message, color):
    text = font.render(message, True, color)
    screen.blit(text, (10, GRID_HEIGHT + 96))   # sits in the third row, below both button rows