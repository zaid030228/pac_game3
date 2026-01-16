"""
Pac-Man Game - Main Entry Point

A fully playable Pac-Man game with:
- Dynamic maze generation using Prim's algorithm
- Three distinct ghost AI algorithms:
  * Blinky: A* pathfinding
  * Pinky: Greedy algorithm with lookahead
  * Clyde: Finite State Machine (CHASE/SCATTER)
- Performance optimizations for stress mode
- Debug visualization

Controls:
- Arrow Keys: Move Pac-Man
- P: Pause/Unpause
- D: Toggle Debug Mode (shows ghost targets)
- S: Toggle Stress Mode (spawns up to 50 ghosts)
- R: Restart (when game over)
- ESC: Quit
"""

from game import Game


def main():
    """Main entry point for the game."""
    print("=" * 60)
    print("PAC-MAN GAME")
    print("=" * 60)
    print("\nControls:")
    print("  Arrow Keys: Move Pac-Man")
    print("  P: Pause/Unpause")
    print("  D: Toggle Debug Mode")
    print("  S: Toggle Stress Mode")
    print("  R: Restart (when game over)")
    print("  ESC: Quit")
    print("\nGhost AI Algorithms:")
    print("  Blinky (Red): A* Pathfinding - O(E log V)")
    print("  Pinky (Pink): Greedy Algorithm - O(1) per decision")
    print("  Clyde (Orange): Finite State Machine - O(1) per check")
    print("\nStarting game...\n")
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
