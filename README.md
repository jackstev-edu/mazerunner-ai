# MazeRunner

An interactive pathfinding visualizer built for Project 0. Claude was used as a coding agent to help implement unfamiliar libraries and Python syntax, while system design and project direction were led by the developer.

- **Intelligence**: Demonstrating three pathfinding algorithms (BFS, Dijkstra, A*) reasoning over a user generated maze and obstacle course with different cost weights.
- **Interaction**: Pick a tool and an algorithm, draw a maze and observe the search animation optimize the path.

## Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

All controls are mouse only, using the buttons below the grid.

| Button | Action |
|---|---|
| Wall / Mud / Erase | Select a tool, then click or drag on the grid |
| Start / End | Select, then click a cell to move it |
| BFS / Dijkstra / A* | Choose which algorithm Run will use |
| Run | Executes the selected algorithm |

## Project structure

| File | Responsibility |
|---|---|
| `pathfinding.py` | BFS, Dijkstra, and A* algorithms called in main.py |
| `grid_state.py` | Generates the user's maze data: walls, mud, start/end, current tool |
| `ui.py` | Gui button and screen layout. Includes brief instructions |
| `main.py` | pygame setup, main loop and animation |


## Algorithms

- BFS: shortest path by step count, ignores mud cost.
- Dijkstra: cheapest path by real cost, explores evenly in every direction.
- A*: same optimality as Dijkstra, biased toward the goal by a heuristic, so it typically explores fewer cells.