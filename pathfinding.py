"""
Pathfinding Utilities
Implements A* algorithm and helper functions for ghost AI
"""

import heapq
from typing import List, Tuple, Optional, Set
from constants import DIRECTIONS, GRID_WIDTH, GRID_HEIGHT


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan distance between two grid positions.
    Time Complexity: O(1)
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def get_neighbors(pos: Tuple[int, int], maze: List[List[bool]]) -> List[Tuple[int, int]]:
    """
    Get valid neighboring tiles (not walls).
    Time Complexity: O(1) - checks 4 neighbors
    """
    x, y = pos
    neighbors = []
    
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        
        # Handle warp tunnels
        if nx < 0:
            nx = GRID_WIDTH - 1
        elif nx >= GRID_WIDTH:
            nx = 0
        
        if 0 <= ny < GRID_HEIGHT and maze[ny][nx]:
            neighbors.append((nx, ny))
    
    return neighbors


def astar_search(start: Tuple[int, int], 
                 goal: Tuple[int, int], 
                 maze: List[List[bool]]) -> Optional[List[Tuple[int, int]]]:
    """
    A* Pathfinding Algorithm
    
    Finds the shortest path from start to goal using A* search.
    
    Time Complexity: O(E log V) where E is edges and V is vertices
    Space Complexity: O(V) for the priority queue and visited set
    
    Args:
        start: Starting position (x, y)
        goal: Target position (x, y)
        maze: 2D grid where True = walkable, False = wall
    
    Returns:
        List of positions forming the path, or None if no path exists
    """
    if not maze[goal[1]][goal[0]]:
        return None  # Goal is a wall
    
    # Priority queue: (f_score, g_score, position, path)
    open_set = [(0, 0, start, [start])]
    visited: Set[Tuple[int, int]] = set()
    
    while open_set:
        f_score, g_score, current, path = heapq.heappop(open_set)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == goal:
            return path
        
        for neighbor in get_neighbors(current, maze):
            if neighbor in visited:
                continue
            
            # Calculate g_score (cost from start)
            new_g = g_score + 1
            
            # Calculate h_score (heuristic - Manhattan distance)
            h_score = manhattan_distance(neighbor, goal)
            
            # f_score = g_score + h_score
            f_score = new_g + h_score
            
            heapq.heappush(open_set, (f_score, new_g, neighbor, path + [neighbor]))
    
    return None  # No path found


def greedy_next_move(current: Tuple[int, int], 
                     target: Tuple[int, int], 
                     maze: List[List[bool]]) -> Optional[Tuple[int, int]]:
    """
    Greedy Algorithm for pathfinding
    
    Chooses the neighbor that minimizes Manhattan distance to target.
    This is a single-step greedy decision, not full pathfinding.
    
    Time Complexity: O(1) - checks 4 neighbors
    Space Complexity: O(1)
    
    Args:
        current: Current position (x, y)
        target: Target position (x, y)
        maze: 2D grid where True = walkable, False = wall
    
    Returns:
        Next position to move to, or None if stuck
    """
    neighbors = get_neighbors(current, maze)
    
    if not neighbors:
        return None
    
    # Find neighbor with minimum Manhattan distance to target
    best_neighbor = None
    best_distance = float('inf')
    
    for neighbor in neighbors:
        distance = manhattan_distance(neighbor, target)
        if distance < best_distance:
            best_distance = distance
            best_neighbor = neighbor
    
    return best_neighbor


def get_direction_towards(current: Tuple[int, int], 
                          target: Tuple[int, int]) -> Tuple[int, int]:
    """
    Get the direction vector from current to target.
    Returns the primary direction (doesn't handle diagonal).
    Time Complexity: O(1)
    """
    dx = target[0] - current[0]
    dy = target[1] - current[1]
    
    # Handle warp tunnel wraparound
    if abs(dx) > GRID_WIDTH // 2:
        dx = -dx if dx > 0 else -dx
    
    if abs(dx) > abs(dy):
        return (1 if dx > 0 else -1, 0)
    elif dy != 0:
        return (0, 1 if dy > 0 else -1)
    
    return (0, 0)
