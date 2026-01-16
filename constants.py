"""
Game Constants and Configuration
All tunable parameters for the Pac-Man game
"""

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900
FPS = 60

# Grid Settings
GRID_WIDTH = 28
GRID_HEIGHT = 31
TILE_SIZE = 25
MAZE_OFFSET_X = 50
MAZE_OFFSET_Y = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_BLUE = (0, 0, 50)
VULNERABLE_GHOST = (0, 0, 255)  # Blue when vulnerable

# Game Settings
INITIAL_LIVES = 3
PELLET_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORE_BASE = 200
BONUS_FRUIT_SCORE = 100

# Pellet Settings
TOTAL_PELLETS = 240
PELLET_SIZE = 3
POWER_PELLET_SIZE = 8
BONUS_FRUIT_1_THRESHOLD = 70
BONUS_FRUIT_2_THRESHOLD = 170

# Ghost Settings (Made easier - Pac-Man faster, ghosts slower)
GHOST_SPEED = 1.2  # Slower ghosts
VULNERABLE_GHOST_SPEED = 0.8  # Even slower when vulnerable
PACMAN_SPEED = 2.5  # Faster Pac-Man for easier escape
VULNERABLE_DURATION = 8000  # Longer vulnerable duration (milliseconds)
FRIGHTENED_DURATION = 10000  # Longer frightened duration

# Ghost AI Settings (Made easier - less aggressive)
BLINKY_UPDATE_INTERVAL = 8  # Slower A* updates (less frequent pathfinding)
PINKY_LOOKAHEAD_TILES = 3  # Shorter lookahead (less accurate prediction)
CLYDE_CHASE_DISTANCE = 6  # Shorter chase distance (switches to scatter sooner)
CLYDE_SCATTER_TARGET = (1, 29)  # Bottom-left corner

# Movement Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Ghost Colors
BLINKY_COLOR = RED
PINKY_COLOR = PINK
INKY_COLOR = CYAN  # Cyan/Light Blue
CLYDE_COLOR = ORANGE

# Stress Mode
STRESS_MODE_MAX_GHOSTS = 50
STRESS_MODE_ENABLED = False  # Toggle with 'S' key

# Debug Mode
DEBUG_MODE = False  # Toggle with 'D' key - shows ghost targets
