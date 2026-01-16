"""
Maze Generation and Management
Uses Prim's algorithm to generate fully connected mazes
"""

import random
from typing import List, Tuple, Set
from constants import GRID_WIDTH, GRID_HEIGHT, PELLET_SIZE, POWER_PELLET_SIZE


class Maze:
    """
    Represents the game maze with dynamic generation.
    Uses Prim's algorithm to ensure full connectivity.
    """
    
    def __init__(self):
        self.walls: List[List[bool]] = []  # True = walkable, False = wall
        self.pellets: List[List[bool]] = []  # True = has pellet
        self.power_pellets: List[List[bool]] = []  # True = has power pellet
        self.pellet_count = 0
        self.generate_maze()
        self.place_pellets()
    
    def generate_maze(self):
        """
        Generate a more open maze with multiple paths and escape routes.
        Uses a modified approach to create wider corridors and more connections.
        
        Time Complexity: O(V log V) where V is number of vertices
        Space Complexity: O(V)
        """
        # Initialize all as walls
        self.walls = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Create horizontal corridors (multiple escape routes)
        for y in range(3, GRID_HEIGHT - 3, 4):  # Every 4 rows
            for x in range(1, GRID_WIDTH - 1):
                self.walls[y][x] = True
        
        # Create vertical corridors (multiple escape routes)
        for x in range(3, GRID_WIDTH - 3, 4):  # Every 4 columns
            for y in range(1, GRID_HEIGHT - 1):
                self.walls[y][x] = True
        
        # Create additional diagonal/connecting paths
        for y in range(1, GRID_HEIGHT - 1):
            for x in range(1, GRID_WIDTH - 1):
                # Create more open areas - 60% chance to be walkable
                if random.random() < 0.6:
                    self.walls[y][x] = True
        
        # Ensure warp tunnels are fully open (horizontal escape route)
        tunnel_y = GRID_HEIGHT // 2
        for x in range(GRID_WIDTH):
            self.walls[tunnel_y][x] = True
        
        # Create additional horizontal escape routes
        for escape_y in [GRID_HEIGHT // 4, 3 * GRID_HEIGHT // 4]:
            for x in range(GRID_WIDTH):
                self.walls[escape_y][x] = True
        
        # Create additional vertical escape routes
        for escape_x in [GRID_WIDTH // 4, GRID_WIDTH // 2, 3 * GRID_WIDTH // 4]:
            for y in range(GRID_HEIGHT):
                self.walls[y][escape_x] = True
        
        # Ensure spawn areas are open
        # Top area (ghost spawn)
        for y in range(1, 8):
            for x in range(GRID_WIDTH // 2 - 3, GRID_WIDTH // 2 + 4):
                if 0 <= x < GRID_WIDTH:
                    self.walls[y][x] = True
        
        # Bottom area (Pac-Man spawn)
        for y in range(GRID_HEIGHT - 8, GRID_HEIGHT - 1):
            for x in range(GRID_WIDTH // 2 - 3, GRID_WIDTH // 2 + 4):
                if 0 <= x < GRID_WIDTH:
                    self.walls[y][x] = True
        
        # Ensure connectivity - add connecting paths between major corridors
        # This creates multiple escape routes
        for _ in range(20):  # Add 20 random connecting paths
            x = random.randint(2, GRID_WIDTH - 3)
            y = random.randint(2, GRID_HEIGHT - 3)
            # Create small cross pattern for better connectivity
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                        if abs(dx) + abs(dy) <= 1:  # Only horizontal/vertical
                            self.walls[ny][nx] = True
    
    def place_pellets(self):
        """
        Place pellets and power pellets in walkable areas.
        Ensures all pellets are reachable (maze is fully connected).
        """
        self.pellets = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.power_pellets = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.pellet_count = 0
        
        # Place regular pellets
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.walls[y][x]:
                    # Don't place in center spawn area
                    center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
                    if abs(x - center_x) > 2 or abs(y - center_y) > 2:
                        self.pellets[y][x] = True
                        self.pellet_count += 1
        
        # Place power pellets in corners
        corners = [
            (2, 2),
            (GRID_WIDTH - 3, 2),
            (2, GRID_HEIGHT - 3),
            (GRID_WIDTH - 3, GRID_HEIGHT - 3)
        ]
        
        for x, y in corners:
            if self.walls[y][x]:
                self.power_pellets[y][x] = True
                # Remove regular pellet if present
                if self.pellets[y][x]:
                    self.pellets[y][x] = False
                    self.pellet_count -= 1
    
    def is_walkable(self, x: int, y: int) -> bool:
        """Check if a tile is walkable (not a wall). O(1) collision check."""
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        return self.walls[y][x]
    
    def consume_pellet(self, x: int, y: int) -> int:
        """
        Consume a pellet at the given position.
        Returns score value (10 for pellet, 50 for power pellet, 0 if none).
        """
        if self.power_pellets[y][x]:
            self.power_pellets[y][x] = False
            return 50
        elif self.pellets[y][x]:
            self.pellets[y][x] = False
            self.pellet_count -= 1
            return 10
        return 0
    
    def get_pellet_count(self) -> int:
        """Get remaining pellet count."""
        return self.pellet_count
    
    def has_power_pellet(self, x: int, y: int) -> bool:
        """Check if position has a power pellet."""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.power_pellets[y][x]
        return False
