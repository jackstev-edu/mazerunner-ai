from collections import deque # Import deque for efficient queue operations

def neighbors(cell, walls, rows, cols):
    row, col = cell
    candidates = [(row -1, col), (row +1, col), (row, col -1), (row, col +1)] # up, down, left, right
    return [c for c in candidates if 0 <= c[0] < rows and 0 <= c[1] < cols and c not in walls]  # in-bounds, not a wall

# Breadth-First Search (BFS) algorithm to find the shortest path from start to end
def bfs(start, end, walls, rows, cols):
    frontier = deque([start])  # queue for BFS
    came_from = {start: None} # dictionary to track the path
    while frontier:
        current = frontier.popleft() # Explore the next cell in the queue
        if current == end: # If we reached the end, reconstruct the path
            break
        for nxt in neighbors(current, walls, rows, cols): 
            if nxt not in came_from: # skip anything already explored
                came_from[nxt] = current # track where we came from
                frontier.append(nxt) # add to the queue for exploration

    if end not in came_from:
        return None # End was not reached, no path exists

    # reconstructting the path from end to start using the came_from dictionary
    path = [end] 
    while path[-1] != start:
        path.append(came_from[path[-1]]) # backtrack using the came_from dictionary
    path.reverse() # reverse the path to get it from start to end
    return path


