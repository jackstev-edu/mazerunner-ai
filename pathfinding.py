from collections import deque # Import deque for efficient queue operations
import heapq # Import heapq to order priority queue

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

# Dijkstra's algorithm to find the shortest path from start to end from BFS
# but with a priority queue to handle weighted graphs
def dijkstra(start, end, walls, mud, rows, cols):
    # initialize priority queue with (cost, cell)
    frontier = [(0, start)] 
    came_from = {start: None} 
    cost_so_far = {start: 0} 

    while frontier:
        current_cost, current = heapq.heappop(frontier) # get the lowest cost cell
        if current_cost > cost_so_far[current]: # 
            continue # skip if we already found a better path
        if current == end:
            break # If we reached the end leave the loop

        for nxt in neighbors(current, walls, rows, cols):
            step_cost = 5 if nxt in mud else 1 # cost of moving to the next cell
            new_cost = current_cost + step_cost # calculate the new cost to reach the
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]: 
                cost_so_far[nxt] = new_cost # update the cost to reach nxt
                came_from[nxt] = current # track where we came from
                heapq.heappush(frontier, (new_cost, nxt)) # add to the priority queue

    if end not in came_from:
        return None # No Path exists

    # reconstructing the path from end to start using the came_from dictionary
    path = [end]
    while path[-1] != start:
        path.append(came_from[path[-1]]) # backtrack using the came_from dictionary
    path.reverse() # From start to end
    return path

# Set up for A* algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Manhattan distance

# A* algorithm to find the shortest path from start to end using a heuristic
def astar(start, end, walls, mud, rows, cols):
    # initialize priority queue with (cost, cell)
    frontier = [(heuristic(start, end), 0, start)] # (f_score, g_score, cell)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current_cost, current = heapq.heappop(frontier) # get the lowest priority cell
        if current_cost > cost_so_far[current]:
            continue # skip if we already found a better path
        if current == end:
            break # If we reached the end leave the loop

        for nxt in neighbors(current, walls, rows, cols):
            step_cost = 5 if nxt in mud else 1 
            new_cost = current_cost + step_cost # calculate the new cost to reach the next cell
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost # update the cost to reach nxt
                priority = new_cost + heuristic(nxt, end) # calculate priority using heuristic
                came_from[nxt] = current # track where we came from
                heapq.heappush(frontier, (priority, new_cost, nxt)) # add to the priority queue

    if end not in came_from:
        return None # No Path exists

    path = [end]
    while path[-1] != start:
        path.append(came_from[path[-1]]) # backtrack using the came_from dictionary
    path.reverse() # From start to end
    return path