"""
Pac-Man Player Class
Handles player movement, collision, and state
"""

from typing import Tuple, Optional
from constants import (
    PACMAN_SPEED, GRID_WIDTH, GRID_HEIGHT, TILE_SIZE,
    MAZE_OFFSET_X, MAZE_OFFSET_Y, YELLOW
)
import math


class PacMan:
    """
    Pac-Man player character with grid-based movement and corner-cutting.
    """
    
    def __init__(self, maze):
        self.maze = maze
        # Start position (bottom-center area, away from ghost spawn)
        self.grid_x = GRID_WIDTH // 2
        self.grid_y = GRID_HEIGHT - 5  # Bottom area, safe from ghosts
        # Ensure position is walkable
        if not self.maze.is_walkable(self.grid_x, self.grid_y):
            # Find nearest walkable position
            for offset in range(1, 10):
                for dx in [-offset, offset]:
                    for dy in [-offset, offset]:
                        test_x = self.grid_x + dx
                        test_y = self.grid_y + dy
                        if (0 <= test_x < GRID_WIDTH and 0 <= test_y < GRID_HEIGHT and
                            self.maze.is_walkable(test_x, test_y)):
                            self.grid_x = test_x
                            self.grid_y = test_y
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
        # Pixel position (center of tile)
        self.pixel_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
        self.pixel_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_Y
        
        self.direction = (0, 0)  # Current movement direction
        self.next_direction = (0, 0)  # Queued direction (for corner-cutting)
        self.speed = PACMAN_SPEED
        self.radius = TILE_SIZE // 2 - 2
        self.angle = 0  # For mouth animation
        
    def update(self):
        """Update Pac-Man position and handle movement."""
        # Try to change direction if queued
        if self.next_direction != (0, 0):
            self._try_change_direction()
        
        # Move in current direction
        if self.direction != (0, 0):
            self._move()
        
        # Update animation angle
        self.angle = (self.angle + 5) % 360
    
    def _move(self):
        """Move Pac-Man based on current direction."""
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
            self.grid_x = grid_x
            self.grid_y = grid_y
        else:
            # Stop if hit wall
            self.direction = (0, 0)
            # Align to grid
            self.pixel_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
            self.pixel_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_Y
    
    def _try_change_direction(self):
        """
        Attempt to change direction (corner-cutting advantage).
        Allows pre-queuing direction changes before reaching intersection.
        """
        dx, dy = self.next_direction
        next_grid_x = self.grid_x + dx
        next_grid_y = self.grid_y + dy
        
        # Handle warp tunnels
        if next_grid_x < 0:
            next_grid_x = GRID_WIDTH - 1
        elif next_grid_x >= GRID_WIDTH:
            next_grid_x = 0
        
        # Check if we're close enough to center of tile to turn
        center_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
        center_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_Y
        
        distance_to_center = math.sqrt(
            (self.pixel_x - center_x) ** 2 + (self.pixel_y - center_y) ** 2
        )
        
        # If close to center and next tile is walkable, change direction
        if distance_to_center < TILE_SIZE * 0.3:
            if self.maze.is_walkable(next_grid_x, next_grid_y):
                self.direction = self.next_direction
                self.next_direction = (0, 0)
    
    def set_direction(self, direction: Tuple[int, int]):
        """Queue a direction change."""
        self.next_direction = direction
    
    def get_grid_pos(self) -> Tuple[int, int]:
        """Get current grid position."""
        return (self.grid_x, self.grid_y)
    
    def get_pixel_pos(self) -> Tuple[float, float]:
        """Get current pixel position."""
        return (self.pixel_x, self.pixel_y)
    
    def get_direction(self) -> Tuple[int, int]:
        """Get current movement direction."""
        return self.direction
    
    def reset_position(self):
        """Reset to starting position (bottom area, safe from ghosts)."""
        self.grid_x = GRID_WIDTH // 2
        self.grid_y = GRID_HEIGHT - 5  # Bottom area
        # Ensure position is walkable
        if not self.maze.is_walkable(self.grid_x, self.grid_y):
            # Find nearest walkable position
            for offset in range(1, 10):
                for dx in [-offset, offset]:
                    for dy in [-offset, offset]:
                        test_x = self.grid_x + dx
                        test_y = self.grid_y + dy
                        if (0 <= test_x < GRID_WIDTH and 0 <= test_y < GRID_HEIGHT and
                            self.maze.is_walkable(test_x, test_y)):
                            self.grid_x = test_x
                            self.grid_y = test_y
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
        self.pixel_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_X
        self.pixel_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2 + MAZE_OFFSET_Y
        self.direction = (0, 0)
        self.next_direction = (0, 0)
