# Pac-Man Game - Python Implementation

A fully playable Pac-Man game built with Python and Pygame, featuring distinct AI algorithms for each ghost, dynamic maze generation, and performance optimizations.

## Architecture Overview

### Core Components

1. **Game Engine** (`game.py`)
   - Main game loop running at 60 FPS
   - State management (playing, paused, game over)
   - Rendering and UI
   - Collision detection
   - Score and lives tracking

2. **Maze System** (`maze.py`)
   - Dynamic maze generation using **Prim's Algorithm**
   - Ensures full connectivity (no isolated regions)
   - Graph-based representation
   - Pellet and power pellet management
   - O(1) collision detection

3. **Pac-Man Player** (`pacman.py`)
   - Grid-based movement with corner-cutting advantage
   - Smooth pixel-perfect movement
   - Warp tunnel support
   - Direction queuing system

4. **Ghost AI System** (`ghost.py`)
   - Base `Ghost` class with common functionality
   - Four distinct AI implementations:
     - **Blinky (Red)**: A* Pathfinding Algorithm
     - **Pinky (Pink)**: Greedy Algorithm with lookahead
     - **Inky (Cyan)**: Vector-based targeting (uses Pac-Man and Blinky positions)
     - **Clyde (Orange)**: Finite State Machine (CHASE/SCATTER)

5. **Pathfinding Utilities** (`pathfinding.py`)
   - A* search algorithm (O(E log V) complexity)
   - Greedy algorithm (O(1) per decision)
   - Manhattan distance calculations
   - Neighbor finding with warp tunnel support

## Ghost AI Algorithms

### Blinky - A* Pathfinding
- **Algorithm**: A* Search
- **Time Complexity**: O(E log V) per path calculation
- **Space Complexity**: O(V)
- **Behavior**: Calculates shortest path to Pac-Man's current position
- **Optimization**: Pathfinding throttled (recalculates every 5 frames)

### Pinky - Greedy Algorithm
- **Algorithm**: Greedy (Manhattan distance minimization)
- **Time Complexity**: O(1) per decision
- **Space Complexity**: O(1)
- **Behavior**: Targets 4 tiles ahead of Pac-Man's current direction
- **Strategy**: Ambush by predicting Pac-Man's movement

### Inky - Vector-Based Targeting
- **Algorithm**: Vector calculation using Pac-Man and Blinky positions
- **Time Complexity**: O(1) per calculation
- **Space Complexity**: O(1)
- **Behavior**: Calculates target 2 tiles ahead of Pac-Man, then doubles the vector from Blinky to that target
- **Strategy**: Creates unpredictable ambush patterns using both player and chaser positions

### Clyde - Finite State Machine
- **Algorithm**: FSM with two states
- **Time Complexity**: O(1) per state check
- **Space Complexity**: O(1)
- **States**:
  - **CHASE**: Targets Pac-Man directly (like Blinky)
  - **SCATTER**: Flees to bottom-left corner when too close (< 6 tiles)
- **State Transition**: Based on distance threshold from Pac-Man

## Performance Optimizations

1. **Spatial Partitioning**: Grid-based collision detection (O(1))
2. **Pathfinding Throttling**: A* recalculates periodically, not every frame
3. **Stress Mode**: Can handle up to 50 ghosts while maintaining ~60 FPS
4. **Memory Management**: Efficient pellet removal, no unnecessary object creation

## Dynamic Maze Generation

- Uses **Prim's Algorithm** to generate fully connected mazes
- Each round creates a new unique maze
- Guarantees all pellets are reachable
- Graph-based representation ensures no isolated regions

## Game Features

- ✅ 240 pellets to collect
- ✅ 4 power pellets (energizers) that make ghosts vulnerable
- ✅ Ghost eating mechanics with score multipliers
- ✅ Warp tunnels on left/right edges
- ✅ Lives system (3 lives)
- ✅ Bonus fruit appearing after 70 and 170 pellets
- ✅ Score tracking
- ✅ Debug mode to visualize ghost targets and states
- ✅ Stress mode for performance testing

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python main.py
```

## Controls

- **Arrow Keys**: Move Pac-Man
- **P**: Pause/Unpause
- **D**: Toggle Debug Mode (shows ghost targets and states)
- **S**: Toggle Stress Mode (spawns up to 50 ghosts)
- **R**: Restart (when game over)
- **ESC**: Quit

## Code Structure

```
pac/
├── main.py           # Entry point
├── game.py           # Main game class and loop
├── maze.py           # Maze generation and management
├── pacman.py         # Pac-Man player class
├── ghost.py          # Ghost AI implementations
├── pathfinding.py    # A* and pathfinding utilities
├── constants.py              # Game configuration
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── COMPLEXITY_ANALYSIS.md    # Big O complexity documentation
├── AI_CRITIQUE_REFLECTION.md # AI interaction log and verification
├── PRESENTATION_GUIDE.md     # Classroom presentation guide
└── PUSH_TO_GITHUB.md        # GitHub setup instructions
```

## Technical Details

### Collision Detection
- O(1) tile-based checks
- Grid-aligned positions for efficient lookups

### Pathfinding Complexity
- **A* (Blinky)**: O(E log V) - documented in code comments
- **Greedy (Pinky)**: O(1) - documented in code comments
- **FSM (Clyde)**: O(1) - documented in code comments

### Memory Management
- Pellets removed efficiently (no object creation in main loop)
- Spatial partitioning reduces collision checks
- Pathfinding results cached and throttled

## Debug Features

Enable debug mode (D key) to see:
- Ghost target tiles (highlighted)
- Lines from ghosts to their targets
- Current AI state for each ghost (CHASE/SCATTER)

## Educational Value

This implementation is designed for educational purposes:
- Clear separation of concerns
- Well-documented algorithms
- Complexity analysis in comments
- Modular design for easy understanding
- Exposed AI state for visualization

## License

This is an educational implementation created for demonstration purposes.
