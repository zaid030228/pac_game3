"""
Ghost Base Class and Specific Implementations
Each ghost uses a different AI algorithm as specified
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from constants import (
    GHOST_SPEED, VULNERABLE_GHOST_SPEED, GRID_WIDTH, GRID_HEIGHT,
    TILE_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y, VULNERABLE_GHOST,
    BLINKY_COLOR, PINKY_COLOR, INKY_COLOR, CLYDE_COLOR, UP, DOWN, LEFT, RIGHT
)
from pathfinding import astar_search, greedy_next_move, manhattan_distance, get_neighbors
import random


class Ghost(ABC):
    """
    Base class for all ghosts.
    Implements common movement and state management.
    """
    
    def __init__(self, maze, start_x: int, start_y: int, color: Tuple[int, int, int], name: str):
        self.maze = maze
        self.name = name
        self.color = color
        self.start_x = start_x
        self.start_y = start_y
        
        # Position
        self.grid_x = start_x
        self.grid_y = start_y
        self.pixel_x = start_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
        self.pixel_y = start_y * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_Y
        
        # Movement
        self.direction = (0, 0)
        self.speed = GHOST_SPEED
        
        # State
        self.vulnerable = False
        self.vulnerable_timer = 0
        self.eaten = False
        
        # AI State (exposed for debugging)
        self.current_state = "CHASE"
        self.target_tile: Optional[Tuple[int, int]] = None
        
        # Pathfinding throttling (for performance)
        self.pathfinding_counter = 0
    
    def update(self, pacman, vulnerable_mode: bool, dt: int):
        """
        Update ghost state and position.
        
        Args:
            pacman: PacMan instance
            vulnerable_mode: Whether power pellet is active
            dt: Delta time in milliseconds
        """
        # Update vulnerable state
        if vulnerable_mode and not self.vulnerable:
            self.vulnerable = True
            self.vulnerable_timer = 0
            # Reverse direction when becoming vulnerable
            self.direction = (-self.direction[0], -self.direction[1])
        elif not vulnerable_mode:
            self.vulnerable = False
            self.vulnerable_timer = 0
        
        if self.vulnerable:
            self.vulnerable_timer += dt
            self.speed = VULNERABLE_GHOST_SPEED
        else:
            self.speed = GHOST_SPEED
        
        # Update AI and movement
        if not self.eaten:
            self._update_ai(pacman)
            self._move()
    
    @abstractmethod
    def _update_ai(self, pacman):
        """
        Abstract method for AI decision making.
        Each ghost implements its own algorithm.
        Must set self.target_tile and self.current_state.
        """
        pass
    
    def _move(self):
        """Move ghost based on current direction."""
        dx, dy = self.direction
        new_pixel_x = self.pixel_x + dx * self.speed
        new_pixel_y = self.pixel_y + dy * self.speed
        
        # Calculate grid position
        grid_x = int((new_pixel_x - MAZE_OFFSET_X) // TILE_SIZE)
        grid_y = int((new_pixel_y - MAZE_OFFSET_Y) // TILE_SIZE)
        
        # Handle warp tunnels
        if grid_x < 0:
            grid_x = GRID_WIDTH - 1
            new_pixel_x = grid_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
        elif grid_x >= GRID_WIDTH:
            grid_x = 0
            new_pixel_x = grid_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
        
        # Check if we can move to new position
        if self.maze.is_walkable(grid_x, grid_y):
            self.pixel_x = new_pixel_x
            self.pixel_y = new_pixel_y
            
            # Check if we've moved to a new tile
            if grid_x != self.grid_x or grid_y != self.grid_y:
                self.grid_x = grid_x
                self.grid_y = grid_y
                # At intersection (new tile) - can change direction
                if self.target_tile:
                    self._choose_direction_at_intersection()
        else:
            # Hit wall - choose new direction
            center_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
            center_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_Y
            self.pixel_x = center_x
            self.pixel_y = center_y
            self._choose_direction_at_intersection()
    
    def _choose_direction_at_intersection(self):
        """Choose direction at intersection (when hitting wall or at center of tile)."""
        # Get valid neighbors (not walls, not opposite direction)
        opposite = (-self.direction[0], -self.direction[1])
        neighbors = get_neighbors((self.grid_x, self.grid_y), self.maze.walls)
        
        # Filter out opposite direction
        valid_directions = []
        for nx, ny in neighbors:
            dx = nx - self.grid_x
            dy = ny - self.grid_y
            if (dx, dy) != opposite:
                valid_directions.append((dx, dy))
        
        if not valid_directions:
            # Dead end - must reverse
            self.direction = opposite
            return
        
        # If vulnerable, choose random direction
        if self.vulnerable:
            self.direction = random.choice(valid_directions)
        else:
            # Choose direction towards target
            if self.target_tile:
                best_dir = None
                best_distance = float('inf')
                
                for dx, dy in valid_directions:
                    next_pos = (self.grid_x + dx, self.grid_y + dy)
                    distance = manhattan_distance(next_pos, self.target_tile)
                    if distance < best_distance:
                        best_distance = distance
                        best_dir = (dx, dy)
                
                if best_dir:
                    self.direction = best_dir
                else:
                    self.direction = random.choice(valid_directions)
            else:
                self.direction = random.choice(valid_directions)
    
    def get_grid_pos(self) -> Tuple[int, int]:
        """Get current grid position."""
        return (self.grid_x, self.grid_y)
    
    def reset_position(self):
        """Reset to starting position."""
        self.grid_x = self.start_x
        self.grid_y = self.start_y
        self.pixel_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
        self.pixel_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_Y
        self.direction = (0, 0)
        self.vulnerable = False
        self.eaten = False


class Blinky(Ghost):
    """
    Blinky - The Chaser
    Uses A* Search Algorithm to find shortest path to Pac-Man.
    
    Algorithm: A* Pathfinding
    Time Complexity: O(E log V) per path calculation
    Space Complexity: O(V)
    """
    
    def __init__(self, maze, start_x: int, start_y: int):
        super().__init__(maze, start_x, start_y, BLINKY_COLOR, "Blinky")
        from constants import BLINKY_UPDATE_INTERVAL
        self.update_interval = BLINKY_UPDATE_INTERVAL
        self.path: Optional[List[Tuple[int, int]]] = None
    
    def _update_ai(self, pacman):
        """Update AI using A* pathfinding."""
        self.current_state = "CHASE"
        
        # Throttle pathfinding for performance
        self.pathfinding_counter += 1
        if self.pathfinding_counter >= self.update_interval:
            self.pathfinding_counter = 0
            
            # Get Pac-Man's current position
            pacman_pos = pacman.get_grid_pos()
            current_pos = (self.grid_x, self.grid_y)
            
            # Calculate path using A*
            self.path = astar_search(current_pos, pacman_pos, self.maze.walls)
            
            if self.path and len(self.path) > 1:
                # Next step in path is our target
                self.target_tile = self.path[1]
            else:
                # Fallback to direct target
                self.target_tile = pacman_pos
        
        # If we have a path, use it; otherwise use target tile
        if self.path and len(self.path) > 1:
            next_pos = self.path[1]
            dx = next_pos[0] - self.grid_x
            dy = next_pos[1] - self.grid_y
            
            # Handle warp tunnel wraparound
            if abs(dx) > GRID_WIDTH // 2:
                dx = -dx if dx > 0 else -dx
            
            if dx != 0 or dy != 0:
                self.direction = (1 if dx > 0 else -1 if dx < 0 else 0,
                                1 if dy > 0 else -1 if dy < 0 else 0)


class Pinky(Ghost):
    """
    Pinky - The Ambusher
    Uses Greedy Algorithm targeting 4 tiles ahead of Pac-Man.
    
    Algorithm: Greedy (Manhattan distance minimization)
    Time Complexity: O(1) per decision
    Space Complexity: O(1)
    """
    
    def __init__(self, maze, start_x: int, start_y: int):
        super().__init__(maze, start_x, start_y, PINKY_COLOR, "Pinky")
        from constants import PINKY_LOOKAHEAD_TILES
        self.lookahead = PINKY_LOOKAHEAD_TILES
    
    def _update_ai(self, pacman):
        """Update AI using greedy algorithm with lookahead."""
        self.current_state = "CHASE"
        
        # Get Pac-Man's position and direction
        pacman_pos = pacman.get_grid_pos()
        pacman_dir = pacman.get_direction()
        
        # Calculate target: 4 tiles ahead of Pac-Man
        if pacman_dir != (0, 0):
            target_x = pacman_pos[0] + pacman_dir[0] * self.lookahead
            target_y = pacman_pos[1] + pacman_dir[1] * self.lookahead
        else:
            # If Pac-Man not moving, target directly
            target_x = pacman_pos[0]
            target_y = pacman_pos[1]
        
        # Clamp to valid range
        target_x = max(0, min(GRID_WIDTH - 1, target_x))
        target_y = max(0, min(GRID_HEIGHT - 1, target_y))
        
        self.target_tile = (target_x, target_y)
        
        # Use greedy algorithm to choose next move
        current_pos = (self.grid_x, self.grid_y)
        next_pos = greedy_next_move(current_pos, self.target_tile, self.maze.walls)
        
        if next_pos:
            dx = next_pos[0] - self.grid_x
            dy = next_pos[1] - self.grid_y
            
            # Handle warp tunnel wraparound
            if abs(dx) > GRID_WIDTH // 2:
                dx = -dx if dx > 0 else -dx
            
            if dx != 0 or dy != 0:
                self.direction = (1 if dx > 0 else -1 if dx < 0 else 0,
                                1 if dy > 0 else -1 if dy < 0 else 0)


class Inky(Ghost):
    """
    Inky - The Bashful Ghost
    Targets a position between Pac-Man and Blinky's position.
    
    Algorithm: Vector-based targeting (uses both Pac-Man and Blinky positions)
    Time Complexity: O(1) per calculation
    Space Complexity: O(1)
    
    Behavior: Inky calculates a target point that is 2 tiles ahead of Pac-Man
    in the direction Pac-Man is facing, then doubles the vector from Blinky
    to that point. This creates unpredictable ambush patterns.
    """
    
    def __init__(self, maze, start_x: int, start_y: int):
        super().__init__(maze, start_x, start_y, INKY_COLOR, "Inky")
        self.blinky_ref = None  # Will be set by game after Blinky is created
    
    def set_blinky_reference(self, blinky):
        """Set Blinky reference for Inky's targeting algorithm."""
        self.blinky_ref = blinky
    
    def _update_ai(self, pacman):
        """
        Update AI using vector calculation based on Pac-Man and Blinky.
        
        Args:
            pacman: PacMan instance
            blinky: Blinky ghost instance (if available)
        """
        self.current_state = "CHASE"
        
        pacman_pos = pacman.get_grid_pos()
        pacman_dir = pacman.get_direction()
        current_pos = (self.grid_x, self.grid_y)
        
        # If Blinky reference is available, use complex targeting
        if self.blinky_ref:
            blinky_pos = self.blinky_ref.get_grid_pos()
            
            # Calculate target 2 tiles ahead of Pac-Man
            if pacman_dir != (0, 0):
                target_ahead_x = pacman_pos[0] + pacman_dir[0] * 2
                target_ahead_y = pacman_pos[1] + pacman_dir[1] * 2
            else:
                target_ahead_x = pacman_pos[0]
                target_ahead_y = pacman_pos[1]
            
            # Double the vector from Blinky to the target ahead of Pac-Man
            # This creates Inky's unique ambush behavior
            vector_x = target_ahead_x - blinky_pos[0]
            vector_y = target_ahead_y - blinky_pos[1]
            
            self.target_tile = (
                blinky_pos[0] + vector_x * 2,
                blinky_pos[1] + vector_y * 2
            )
        else:
            # Fallback: target 2 tiles ahead of Pac-Man
            if pacman_dir != (0, 0):
                self.target_tile = (
                    pacman_pos[0] + pacman_dir[0] * 2,
                    pacman_pos[1] + pacman_dir[1] * 2
                )
            else:
                self.target_tile = pacman_pos
        
        # Clamp target to valid range
        self.target_tile = (
            max(0, min(GRID_WIDTH - 1, self.target_tile[0])),
            max(0, min(GRID_HEIGHT - 1, self.target_tile[1]))
        )
        
        # Use greedy algorithm to move towards target
        next_pos = greedy_next_move(current_pos, self.target_tile, self.maze.walls)
        
        if next_pos:
            dx = next_pos[0] - self.grid_x
            dy = next_pos[1] - self.grid_y
            
            # Handle warp tunnel wraparound
            if abs(dx) > GRID_WIDTH // 2:
                dx = -dx if dx > 0 else -dx
            
            if dx != 0 or dy != 0:
                self.direction = (1 if dx > 0 else -1 if dx < 0 else 0,
                                1 if dy > 0 else -1 if dy < 0 else 0)


class Clyde(Ghost):
    """
    Clyde - The Stateful Ghost
    Uses Finite State Machine with CHASE and SCATTER states.
    
    Algorithm: Finite State Machine
    States:
    - CHASE: Behaves like Blinky (targets Pac-Man)
    - SCATTER: Flees to bottom-left corner
    
    Time Complexity: O(1) per state transition check
    Space Complexity: O(1)
    """
    
    def __init__(self, maze, start_x: int, start_y: int):
        super().__init__(maze, start_x, start_y, CLYDE_COLOR, "Clyde")
        from constants import CLYDE_CHASE_DISTANCE, CLYDE_SCATTER_TARGET
        self.chase_distance = CLYDE_CHASE_DISTANCE
        self.scatter_target = CLYDE_SCATTER_TARGET
        self.state = "CHASE"
    
    def _update_ai(self, pacman):
        """Update AI using Finite State Machine."""
        pacman_pos = pacman.get_grid_pos()
        current_pos = (self.grid_x, self.grid_y)
        distance = manhattan_distance(current_pos, pacman_pos)
        
        # State transition logic
        if self.state == "CHASE":
            if distance < self.chase_distance:
                # Too close - switch to SCATTER
                self.state = "SCATTER"
                self.current_state = "SCATTER"
                self.target_tile = self.scatter_target
            else:
                # Far enough - continue CHASE
                self.current_state = "CHASE"
                self.target_tile = pacman_pos
        else:  # SCATTER
            if distance >= self.chase_distance:
                # Far enough - switch to CHASE
                self.state = "CHASE"
                self.current_state = "CHASE"
                self.target_tile = pacman_pos
            else:
                # Still too close - continue SCATTER
                self.current_state = "SCATTER"
                self.target_tile = self.scatter_target
        
        # Choose direction towards target using greedy approach
        next_pos = greedy_next_move(current_pos, self.target_tile, self.maze.walls)
        
        if next_pos:
            dx = next_pos[0] - self.grid_x
            dy = next_pos[1] - self.grid_y
            
            # Handle warp tunnel wraparound
            if abs(dx) > GRID_WIDTH // 2:
                dx = -dx if dx > 0 else -dx
            
            if dx != 0 or dy != 0:
                self.direction = (1 if dx > 0 else -1 if dx < 0 else 0,
                                1 if dy > 0 else -1 if dy < 0 else 0)
