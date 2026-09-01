# ui.py
# Button layout and drawing for the on-screen toolbar. Takes whatever it
# needs (screen, font, which option is active) as arguments instead of
# reaching into grid_state or main directly, keeps it reusable.

import pygame
from grid_state import ROWS, CELL_SIZE

GRID_HEIGHT = ROWS * CELL_SIZE # 480
UI_HEIGHT = 240 # room for three sections plus a status row

# Y positions for each section, computed from GRID_HEIGHT so they'd scale if the grid ever changed size
TOOLS_HEADING_Y = GRID_HEIGHT + 8
TOOLS_BUTTON_Y = GRID_HEIGHT + 26
TOOLS_BLURB_Y = GRID_HEIGHT + 62
DIVIDER_1_Y = GRID_HEIGHT + 82

ALGO_HEADING_Y = GRID_HEIGHT + 90
ALGO_BUTTON_Y = GRID_HEIGHT + 108
ALGO_BLURB_Y = GRID_HEIGHT + 144
DIVIDER_2_Y = GRID_HEIGHT + 164

ACTIONS_BUTTON_Y = GRID_HEIGHT + 172
DIVIDER_3_Y = GRID_HEIGHT + 208

STATUS_Y = GRID_HEIGHT + 216

TOOL_BUTTONS = [
    {"label": "Wall",  "tool": "wall",  "rect": pygame.Rect(10, TOOLS_BUTTON_Y, 100, 32),
     "blurb": "Blocks the path completely, impassable"},
    {"label": "Mud",   "tool": "mud",   "rect": pygame.Rect(120, TOOLS_BUTTON_Y, 100, 32),
     "blurb": "Costs 5x to cross, slows the path down"},
    {"label": "Erase", "tool": "erase", "rect": pygame.Rect(230, TOOLS_BUTTON_Y, 100, 32),
     "blurb": "Clears a wall or mud back to open ground"},
]

ALGO_BUTTONS = [
    {"label": "BFS",      "algo": "bfs",      "rect": pygame.Rect(10, ALGO_BUTTON_Y, 100, 32),
     "blurb": "Shortest path by step count, ignores mud cost"},
    {"label": "Dijkstra", "algo": "dijkstra", "rect": pygame.Rect(120, ALGO_BUTTON_Y, 120, 32),
     "blurb": "Cheapest path by real cost, explores every direction"},
    {"label": "A*",       "algo": "astar",    "rect": pygame.Rect(250, ALGO_BUTTON_Y, 100, 32),
     "blurb": "Cheapest path, guided toward the goal"},
]

ACTION_BUTTONS = [
    {"label": "Start", "tool": "start", "rect": pygame.Rect(10, ACTIONS_BUTTON_Y, 100, 32)},
    {"label": "End",   "tool": "end",   "rect": pygame.Rect(120, ACTIONS_BUTTON_Y, 100, 32)},
]

RUN_BUTTON = pygame.Rect(230, ACTIONS_BUTTON_Y, 100, 32)

def draw_panel_background(screen):
    panel_rect = pygame.Rect(0, GRID_HEIGHT, screen.get_width(), UI_HEIGHT)
    pygame.draw.rect(screen, (19, 42, 82), panel_rect)          # lighter navy, separates toolbar from grid
    for y in (GRID_HEIGHT, DIVIDER_1_Y, DIVIDER_2_Y, DIVIDER_3_Y):
        pygame.draw.line(screen, (42, 82, 136), (0, y), (screen.get_width(), y), width=1)  # section dividers

def draw_heading(screen, small_font, text, y):
    label = small_font.render(text.upper(), True, (95, 212, 232))  # cyan, reads as a section title
    screen.blit(label, (10, y))

def draw_blurb(screen, small_font, text, y):
    if text:  # skip drawing if there's nothing to show for the current selection
        label = small_font.render(text, True, (143, 166, 204))
        screen.blit(label, (10, y))

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

def draw_run_button(screen, font, rect, hover=False):
    color = (130, 224, 158) if hover else (98, 209, 130)   # green, brighter on hover, distinct from toggle buttons
    pygame.draw.rect(screen, color, rect, border_radius=4)
    text = font.render("Run", True, (10, 30, 15))            # dark text reads better against bright green
    screen.blit(text, text.get_rect(center=rect.center))

def draw_status(screen, small_font, message, color):
    text = small_font.render(message, True, color)
    screen.blit(text, (10, STATUS_Y))

def get_blurb(buttons, key, current_value):
    for b in buttons:
        if b[key] == current_value:
            return b["blurb"]
    return ""  # current selection isn't in this button group, e.g. tool is "start", not a Tools button