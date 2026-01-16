"""
Main Game Class
Handles game loop, state management, rendering, and game logic
"""

import pygame
import random
from typing import List, Optional
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK, WHITE, YELLOW,
    PELLET_SIZE, POWER_PELLET_SIZE, PELLET_SCORE, POWER_PELLET_SCORE,
    GHOST_SCORE_BASE, BONUS_FRUIT_SCORE, INITIAL_LIVES,
    BONUS_FRUIT_1_THRESHOLD, BONUS_FRUIT_2_THRESHOLD,
    GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y,
    VULNERABLE_GHOST, DEBUG_MODE, STRESS_MODE_ENABLED, STRESS_MODE_MAX_GHOSTS
)
from maze import Maze
from pacman import PacMan
from ghost import Blinky, Pinky, Inky, Clyde, Ghost


class Game:
    """
    Main game controller.
    Manages game state, rendering, and game loop.
    """
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.running = True
        self.paused = False
        self.game_over = False
        self.score = 0
        self.lives = INITIAL_LIVES
        self.pellets_consumed = 0
        self.vulnerable_mode = False
        self.vulnerable_timer = 0
        self.ghost_eaten_count = 0  # For scoring multiplier
        
        # Game objects
        self.maze = None
        self.pacman = None
        self.ghosts: List[Ghost] = []
        self.bonus_fruit_active = False
        self.bonus_fruit_pos: Optional[tuple] = None
        self.bonus_fruit_timer = 0
        
        # Stress mode
        self.stress_mode = STRESS_MODE_ENABLED
        self.debug_mode = DEBUG_MODE
        
        self.reset_game()
    
    def reset_game(self):
        """Reset game to initial state."""
        # Generate new maze
        self.maze = Maze()
        
        # Create Pac-Man
        self.pacman = PacMan(self.maze)
        
        # Create ghosts
        self.ghosts = []
        # Spawn ghosts in top area (ghost house), far from Pac-Man
        ghost_house_x = GRID_WIDTH // 2
        ghost_house_y = 5  # Top area
        
        # Spawn ghosts in a small area at the top (4 ghosts total)
        spawn_positions = [
            (ghost_house_x - 1, ghost_house_y),
            (ghost_house_x + 1, ghost_house_y),
            (ghost_house_x, ghost_house_y - 1),
            (ghost_house_x, ghost_house_y + 1)
        ]
        
        # Ensure spawn positions are walkable, find alternatives if needed
        valid_spawns = []
        for x, y in spawn_positions:
            if self.maze.is_walkable(x, y):
                valid_spawns.append((x, y))
            else:
                # Find nearest walkable position
                found = False
                for offset in range(1, 5):
                    for dx in [-offset, offset]:
                        for dy in [-offset, offset]:
                            test_x = x + dx
                            test_y = y + dy
                            if (0 <= test_x < GRID_WIDTH and 0 <= test_y < GRID_HEIGHT and
                                self.maze.is_walkable(test_x, test_y) and
                                (test_x, test_y) not in valid_spawns):
                                valid_spawns.append((test_x, test_y))
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
        
        # Create all 4 ghosts at valid spawn positions
        blinky = None
        inky = None
        if len(valid_spawns) >= 1:
            blinky = Blinky(self.maze, valid_spawns[0][0], valid_spawns[0][1])
            self.ghosts.append(blinky)
        if len(valid_spawns) >= 2:
            self.ghosts.append(Pinky(self.maze, valid_spawns[1][0], valid_spawns[1][1]))
        if len(valid_spawns) >= 3:
            inky = Inky(self.maze, valid_spawns[2][0], valid_spawns[2][1])
            self.ghosts.append(inky)
        if len(valid_spawns) >= 4:
            self.ghosts.append(Clyde(self.maze, valid_spawns[3][0], valid_spawns[3][1]))
        
        # Set Blinky reference for Inky's complex targeting algorithm
        if inky and blinky:
            inky.set_blinky_reference(blinky)
        
        # Stress mode: add more ghosts
        if self.stress_mode:
            for i in range(3, min(STRESS_MODE_MAX_GHOSTS, len(spawn_positions) + 47)):
                x = random.randint(1, GRID_WIDTH - 2)
                y = random.randint(1, GRID_HEIGHT - 2)
                if self.maze.is_walkable(x, y):
                    # Alternate ghost types for variety
                    ghost_type = i % 3
                    if ghost_type == 0:
                        self.ghosts.append(Blinky(self.maze, x, y))
                    elif ghost_type == 1:
                        self.ghosts.append(Pinky(self.maze, x, y))
                    else:
                        self.ghosts.append(Clyde(self.maze, x, y))
        
        # Reset state
        self.vulnerable_mode = False
        self.vulnerable_timer = 0
        self.ghost_eaten_count = 0
        self.pellets_consumed = 0
        self.bonus_fruit_active = False
        self.bonus_fruit_pos = None
        self.bonus_fruit_timer = 0
    
    def handle_events(self):
        """Handle keyboard and window events."""
        from constants import UP, DOWN, LEFT, RIGHT
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.score = 0
                    self.lives = INITIAL_LIVES
                    self.game_over = False
                    self.reset_game()
                elif event.key == pygame.K_s:
                    # Toggle stress mode
                    self.stress_mode = not self.stress_mode
                    self.reset_game()
                elif event.key == pygame.K_d:
                    # Toggle debug mode
                    self.debug_mode = not self.debug_mode
                elif not self.paused and not self.game_over:
                    if event.key == pygame.K_UP:
                        self.pacman.set_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.set_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.set_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.set_direction(RIGHT)
    
    def update(self, dt: int):
        """Update game state."""
        if self.paused or self.game_over:
            return
        
        # Update vulnerable mode timer
        if self.vulnerable_mode:
            self.vulnerable_timer += dt
            from constants import VULNERABLE_DURATION
            if self.vulnerable_timer >= VULNERABLE_DURATION:
                self.vulnerable_mode = False
                self.vulnerable_timer = 0
                self.ghost_eaten_count = 0
        
        # Update Pac-Man
        self.pacman.update()
        
        # Check pellet consumption
        pacman_grid = self.pacman.get_grid_pos()
        pellet_score = self.maze.consume_pellet(pacman_grid[0], pacman_grid[1])
        
        if pellet_score > 0:
            self.score += pellet_score
            if pellet_score == POWER_PELLET_SCORE:
                # Power pellet consumed
                self.vulnerable_mode = True
                self.vulnerable_timer = 0
                self.ghost_eaten_count = 0
            else:
                self.pellets_consumed += 1
        
        # Check bonus fruit
        if (self.pellets_consumed == BONUS_FRUIT_1_THRESHOLD or 
            self.pellets_consumed == BONUS_FRUIT_2_THRESHOLD):
            if not self.bonus_fruit_active:
                # Spawn bonus fruit
                self.bonus_fruit_active = True
                # Place fruit near center
                center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
                self.bonus_fruit_pos = (center_x, center_y)
                self.bonus_fruit_timer = 0
        
        if self.bonus_fruit_active:
            self.bonus_fruit_timer += dt
            if self.bonus_fruit_timer > 10000:  # 10 seconds
                self.bonus_fruit_active = False
                self.bonus_fruit_pos = None
        
        # Check bonus fruit collection
        if self.bonus_fruit_active and self.bonus_fruit_pos:
            if pacman_grid == self.bonus_fruit_pos:
                self.score += BONUS_FRUIT_SCORE
                self.bonus_fruit_active = False
                self.bonus_fruit_pos = None
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.pacman, self.vulnerable_mode, dt)
        
        # Check ghost collisions
        pacman_pos = self.pacman.get_grid_pos()
        for ghost in self.ghosts:
            ghost_pos = ghost.get_grid_pos()
            if pacman_pos == ghost_pos:
                if ghost.vulnerable:
                    # Eat ghost
                    self.ghost_eaten_count += 1
                    self.score += GHOST_SCORE_BASE * self.ghost_eaten_count
                    ghost.eaten = True
                    ghost.reset_position()
                else:
                    # Pac-Man dies
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        # Reset positions
                        self.pacman.reset_position()
                        for g in self.ghosts:
                            g.reset_position()
                        self.vulnerable_mode = False
                        self.vulnerable_timer = 0
        
        # Check win condition
        if self.maze.get_pellet_count() == 0:
            # Level complete - generate new maze
            self.reset_game()
    
    def render(self):
        """Render all game elements."""
        self.screen.fill(BLACK)
        
        # Draw maze
        self._draw_maze()
        
        # Draw bonus fruit
        if self.bonus_fruit_active and self.bonus_fruit_pos:
            x, y = self.bonus_fruit_pos
            pixel_x = x * TILE_SIZE + MAZE_OFFSET_X
            pixel_y = y * TILE_SIZE + MAZE_OFFSET_Y
            pygame.draw.circle(self.screen, YELLOW, (pixel_x, pixel_y), 8)
        
        # Draw ghosts
        for ghost in self.ghosts:
            if not ghost.eaten:
                self._draw_ghost(ghost)
        
        # Draw Pac-Man
        self._draw_pacman()
        
        # Draw debug info
        if self.debug_mode:
            self._draw_debug_info()
        
        # Draw UI
        self._draw_ui()
        
        pygame.display.flip()
    
    def _draw_maze(self):
        """Draw maze walls and pellets."""
        # Draw walls
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pixel_x = x * TILE_SIZE + MAZE_OFFSET_X
                pixel_y = y * TILE_SIZE + MAZE_OFFSET_Y
                
                if not self.maze.is_walkable(x, y):
                    # Draw wall
                    pygame.draw.rect(self.screen, (0, 0, 100),
                                   (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                else:
                    # Draw pellets
                    if self.maze.pellets[y][x]:
                        pygame.draw.circle(self.screen, WHITE,
                                         (pixel_x + TILE_SIZE // 2,
                                          pixel_y + TILE_SIZE // 2),
                                         PELLET_SIZE)
                    elif self.maze.power_pellets[y][x]:
                        pygame.draw.circle(self.screen, WHITE,
                                         (pixel_x + TILE_SIZE // 2,
                                          pixel_y + TILE_SIZE // 2),
                                         POWER_PELLET_SIZE)
    
    def _draw_pacman(self):
        """Draw Pac-Man with mouth animation."""
        px, py = self.pacman.get_pixel_pos()
        radius = self.pacman.radius
        
        # Calculate mouth angle based on direction
        if self.pacman.direction == (1, 0):  # Right
            start_angle = 30
            end_angle = 330
        elif self.pacman.direction == (-1, 0):  # Left
            start_angle = 210
            end_angle = 150
        elif self.pacman.direction == (0, -1):  # Up
            start_angle = 120
            end_angle = 60
        elif self.pacman.direction == (0, 1):  # Down
            start_angle = 300
            end_angle = 240
        else:
            start_angle = 30
            end_angle = 330
        
        # Draw Pac-Man as a circle with a mouth
        pygame.draw.circle(self.screen, YELLOW, (int(px), int(py)), radius)
        # Draw mouth (simplified - just a triangle cutout)
        import math
        mouth_angle = math.radians(start_angle)
        mouth_x = px + radius * math.cos(mouth_angle)
        mouth_y = py - radius * math.sin(mouth_angle)
        pygame.draw.polygon(self.screen, BLACK,
                          [(int(px), int(py)),
                           (int(mouth_x), int(mouth_y)),
                           (int(px + radius * math.cos(math.radians(end_angle))),
                            int(py - radius * math.sin(math.radians(end_angle))))])
    
    def _draw_ghost(self, ghost: Ghost):
        """Draw ghost with appropriate color."""
        px, py = ghost.pixel_x, ghost.pixel_y
        radius = TILE_SIZE // 2 - 2
        
        # Choose color based on state
        if ghost.vulnerable:
            color = VULNERABLE_GHOST
        else:
            color = ghost.color
        
        # Draw ghost body (circle)
        pygame.draw.circle(self.screen, color, (int(px), int(py)), radius)
        
        # Draw eyes (two white circles)
        eye_offset = radius // 3
        pygame.draw.circle(self.screen, WHITE, (int(px - eye_offset), int(py)), radius // 3)
        pygame.draw.circle(self.screen, WHITE, (int(px + eye_offset), int(py)), radius // 3)
        pygame.draw.circle(self.screen, BLACK, (int(px - eye_offset), int(py)), radius // 6)
        pygame.draw.circle(self.screen, BLACK, (int(px + eye_offset), int(py)), radius // 6)
    
    def _draw_debug_info(self):
        """Draw debug information (ghost targets, states)."""
        for ghost in self.ghosts:
            if ghost.target_tile:
                # Draw target tile
                tx, ty = ghost.target_tile
                pixel_x = tx * TILE_SIZE + MAZE_OFFSET_X
                pixel_y = ty * TILE_SIZE + MAZE_OFFSET_Y
                pygame.draw.rect(self.screen, ghost.color,
                               (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 2)
                
                # Draw line from ghost to target
                gx, gy = ghost.pixel_x, ghost.pixel_y
                pygame.draw.line(self.screen, ghost.color,
                               (int(gx), int(gy)),
                               (pixel_x + TILE_SIZE // 2, pixel_y + TILE_SIZE // 2), 1)
            
            # Draw state text
            state_text = self.small_font.render(
                f"{ghost.name}: {ghost.current_state}", True, WHITE)
            self.screen.blit(state_text, (10, 100 + self.ghosts.index(ghost) * 20))
    
    def _draw_ui(self):
        """Draw user interface (score, lives, etc.)."""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))
        
        # Pellets remaining
        pellets_text = self.small_font.render(
            f"Pellets: {self.maze.get_pellet_count()}", True, WHITE)
        self.screen.blit(pellets_text, (WINDOW_WIDTH - 150, 10))
        
        # Vulnerable mode indicator
        if self.vulnerable_mode:
            vulnerable_text = self.small_font.render("VULNERABLE!", True, YELLOW)
            self.screen.blit(vulnerable_text, (WINDOW_WIDTH - 200, 40))
        
        # Game over
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # Paused
        if self.paused:
            paused_text = self.font.render("PAUSED", True, WHITE)
            text_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(paused_text, text_rect)
        
        # Mode indicators
        if self.stress_mode:
            stress_text = self.small_font.render("STRESS MODE", True, (255, 0, 0))
            self.screen.blit(stress_text, (WINDOW_WIDTH - 150, 70))
        
        if self.debug_mode:
            debug_text = self.small_font.render("DEBUG MODE", True, (0, 255, 0))
            self.screen.blit(debug_text, (WINDOW_WIDTH - 150, 90))
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
