# Presentation Guide - Pac-Man Game

## Quick Start for Classroom Presentation

### 1. Running the Game
```bash
cd /Users/macbookpro/Desktop/pac
python3 main.py
```

### 2. Controls During Presentation
- **Arrow Keys**: Move Pac-Man (show gameplay)
- **D**: Toggle Debug Mode (show ghost targets and AI states)
- **S**: Toggle Stress Mode (demonstrate 50 ghosts)
- **P**: Pause (explain while paused)

---

## Presentation Outline (5-10 minutes)

### 1. Introduction (1 minute)
- **Project**: Pac-Man game with distinct AI algorithms
- **Goal**: Demonstrate algorithmic diversity in game AI
- **Technologies**: Python, Pygame, Graph algorithms, Pathfinding

### 2. Algorithmic Diversity - Ghost AI (3-4 minutes)

#### Blinky (Red) - A* Pathfinding
**What to show:**
- Enable Debug Mode (D key)
- Point out Blinky's target tile (red square)
- Explain: "Blinky uses A* search to find shortest path to Pac-Man"
- **Complexity**: O(E log V) - documented in code

**Code to show**: `pathfinding.py:astar_search()` (lines 35-78)

---

#### Pinky (Pink) - Greedy Algorithm
**What to show:**
- Point out Pinky's target (pink square ahead of Pac-Man)
- Explain: "Pinky targets 4 tiles ahead using greedy Manhattan distance"
- **Complexity**: O(1) per decision

**Code to show**: `pathfinding.py:greedy_next_move()` (lines 81-108)

---

#### Inky (Cyan) - Vector-Based Targeting
**What to show:**
- Explain: "Inky uses both Pac-Man and Blinky positions"
- Formula: Target = Blinky + 2×(TargetAhead - Blinky)
- Creates unpredictable ambush patterns

**Code to show**: `ghost.py:Inky._update_ai()` (lines 312-376)

---

#### Clyde (Orange) - Finite State Machine
**What to show:**
- Toggle debug to show state: "CHASE" or "SCATTER"
- Explain: "Clyde switches states based on distance threshold"
- Close to Pac-Man → SCATTER (flees)
- Far from Pac-Man → CHASE (attacks)

**Code to show**: `ghost.py:Clyde._update_ai()` (lines 391-436)

---

### 3. Complexity Analysis (2 minutes)

**Show on screen**: `COMPLEXITY_ANALYSIS.md`

**Key Points**:
- Collision Detection: **O(1)** - direct array access
- A* Pathfinding: **O(E log V)** - priority queue
- Greedy Algorithm: **O(1)** - checks 4 neighbors only
- FSM: **O(1)** - single distance calculation

**Visual Demo**: 
- Show maze size (28×31 = 868 tiles)
- Explain how O(1) collision beats O(n) distance checks

---

### 4. Performance Optimization - Stress Mode (2 minutes)

**What to show**:
1. Normal mode: 4 ghosts, 60 FPS
2. Press **S** to enable Stress Mode
3. Show 50 ghosts still running at ~60 FPS

**Optimizations to explain**:

**a) Pathfinding Throttling**
- Blinky recalculates A* every 8 frames (not every frame)
- Reduces A* calls by 87.5%
- **Code**: `constants.py:BLINKY_UPDATE_INTERVAL = 8`

**b) Spatial Partitioning**
- Grid-based collision: O(1) lookups
- No distance calculations needed
- **Code**: `maze.py:is_walkable()`

**c) Memory Management**
- Pellets: Array flags (no objects)
- Ghosts: Reuse objects (reset instead of recreate)
- **Code**: `maze.py:consume_pellet()`, `ghost.py:reset_position()`

---

### 5. Dynamic Maze Generation (1-2 minutes)

**What to show**:
- Complete a level (eat all pellets)
- New maze generates automatically
- Each maze is different but fully connected

**Algorithm**: Prim's Algorithm
- Creates minimum spanning tree
- Guarantees connectivity (no isolated areas)
- **Code**: `maze.py:generate_maze()`

**Graph Theory**:
- Maze = Connected graph
- All pellets reachable
- Valid spanning tree guarantees navigability

---

### 6. AI Critique Reflection (1 minute)

**Show**: `AI_CRITIQUE_REFLECTION.md`

**Key Points**:
- Verified all algorithms against textbooks
- Manual tracing of A* on 5×5 grid (documented)
- Found and corrected AI suggestions:
  - Pinky: Changed from full paths to O(1) greedy
  - Pathfinding throttling for optimization

---

## Demo Flow Recommendation

1. **Start game** → Show normal gameplay (30 seconds)
2. **Press D** → Enable debug mode, explain ghost targets (1 minute)
3. **Pause (P)** → Show code for each ghost AI (2 minutes)
4. **Unpause** → Play briefly, show different behaviors (30 seconds)
5. **Press S** → Enable stress mode, explain optimization (1 minute)
6. **Show complexity doc** → Explain Big O analysis (1 minute)
7. **Complete level** → Show dynamic maze generation (30 seconds)
8. **Q&A** (remaining time)

---

## Key Code Files to Have Open

1. `ghost.py` - All 4 ghost implementations
2. `pathfinding.py` - A* and greedy algorithms
3. `maze.py` - Prim's algorithm for maze generation
4. `COMPLEXITY_ANALYSIS.md` - Complexity documentation
5. `constants.py` - Show optimization settings

---

## Common Questions & Answers

**Q: Why is Blinky slower than others?**
A: A* is expensive (O(E log V)). We throttle it to every 8 frames for performance.

**Q: How do you verify the algorithms are correct?**
A: Manual tracing (documented in AI_CRITIQUE_REFLECTION.md) and testing with debug mode.

**Q: Can you add more ghosts?**
A: Yes! Stress mode supports up to 50 ghosts (configurable in constants.py).

**Q: Is the maze always solvable?**
A: Yes! Prim's algorithm guarantees a connected graph (no isolated regions).

**Q: What happens if pathfinding fails?**
A: Fallback to direct targeting (manhattan distance) ensures ghosts always move.

---

## Tips for Presentation

1. **Practice the demo** - Know which keys to press
2. **Have code open** - Be ready to show specific algorithms
3. **Explain complexity** - Use the complexity analysis doc
4. **Show debug mode** - Visual aids help understanding
5. **Demonstrate stress mode** - Shows real-world optimization

---

## Files Checklist

✅ All code files present and working
✅ COMPLEXITY_ANALYSIS.md - Big O documentation
✅ AI_CRITIQUE_REFLECTION.md - AI interaction log
✅ README.md - Project documentation
✅ requirements.txt - Dependencies
✅ Game runs at 60 FPS
✅ Debug mode works (D key)
✅ Stress mode works (S key)
✅ All 4 ghosts implemented with distinct algorithms

---

**Good luck with your presentation! 🎮**
