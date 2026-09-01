# grid_state.py
# The maze's raw data: which cells are walls or mud, where start/end sit,
# and which tool is currently selected. No pygame drawing here on purpose --
# kept separate from how it's rendered.

COLS, ROWS, CELL_SIZE = 25, 15, 32  # 25*32=800, 15*32=480 = grid tiles

# Initialization of user interfacing maze elements
walls = set()  # empty set of wall coordinates, to be filled later
mud = set()  # empty set of mud coordinates, to be filled later
start = (2,2) # Maze starting point
end = (ROWS-3, COLS-3) # Maze ending point
tool = "wall" # current tool selected for painting

# translating pixel coordinates to grid coordinates
def cell_at_pixel(pos): 
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

# Function to apply one tool at a time to a cell, based on the current tool selected
def apply_tool(cell):
    global start, end  # Updating preinitialized start and end points - hence "global"
    if tool == "wall":
        mud.discard(cell)  # Discard obstabcle before overriding with wall
        walls.add(cell)           # always adds -- never removes, even if touched twice in one drag
    elif tool == "mud":
        walls.discard(cell)  # Discard obstabcle before overriding with mud
        mud.add(cell)
    elif tool == "erase": # Indiscriminate removal of any obstacles from the cell
        walls.discard(cell)
        mud.discard(cell)
    elif tool == "start": # Update start point to clicked cell
        start = cell
    elif tool == "end": # Update end point to clicked cell
        end = cell