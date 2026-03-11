# 🧩 A-Maze-ing — Complete Learning Guide

> **How to use this file:** Open in Obsidian. Every section builds on the previous one. Read the concept explanations before attempting each step. The code comes from YOU — this guide teaches you *what* and *why*, not just *how*.

---

## 📋 Table of Contents

- [[#Project Overview]]
- [[#Phase 1 — Python Foundations You Must Know]]
- [[#Phase 2 — Understanding Maze Theory]]
- [[#Phase 3 — Project Architecture]]
- [[#Phase 4 — Step-by-Step Implementation Plan]]
- [[#Phase 5 — Visual Representation]]
- [[#Phase 6 — Reusable Package (mazegen)]]
- [[#Phase 7 — Bonus Features]]
- [[#Phase 8 — README & Submission Checklist]]
- [[#Concepts Quick Reference]]

---

## Project Overview

The project asks you to build a **maze generator** in Python that:
1. Reads a config file
2. Generates a valid maze (optionally "perfect")
3. Writes the maze to a file in a specific hexadecimal format
4. Displays it visually (terminal or graphical)
5. Embeds a hidden **"42" pattern** made of closed cells
6. Packages the generation logic as a reusable pip-installable module

---

## Phase 1 — Python Foundations You Must Know

Before writing a single line of maze code, make sure you understand these concepts. Each one is used directly in this project.

---

### 1.1 Type Hints & `mypy`

**What it is:** Python lets you annotate variable and function types. These are optional at runtime, but `mypy` can check them statically.

**Why you need it:** The subject *requires* type hints on all functions and variables, and they must pass `mypy` without errors.

**Concepts to learn:**
- Basic annotations: `def foo(x: int) -> str:`
- The `typing` module: `List`, `Dict`, `Tuple`, `Optional`, `Union`
- In Python 3.10+, you can use `list[int]` directly instead of `List[int]`
- `Optional[X]` means the value can be `X` or `None`

**Example concept:**
```
# Without type hints
def get_cell(grid, x, y):
    return grid[y][x]

# With type hints
def get_cell(grid: list[list[int]], x: int, y: int) -> int:
    return grid[y][x]
```

**To study:** Python docs on `typing`, mypy documentation

---

### 1.2 Docstrings (PEP 257)

**What it is:** Documentation strings placed at the start of functions, classes, or modules.

**Why you need it:** The subject requires Google or NumPy style docstrings on all functions and classes.

**Google style example concept:**
```
def generate(width: int, height: int) -> list[list[int]]:
    """Generate a maze grid.

    Args:
        width: Number of columns.
        height: Number of rows.

    Returns:
        A 2D list of integers encoding wall states.
    """
```

---

### 1.3 Exception Handling

**What it is:** Using `try/except` to catch errors instead of letting the program crash.

**Why you need it:** The subject says the program must NEVER crash. All errors (bad config, wrong file, impossible parameters) must be caught and shown as clear messages.

**Concepts to learn:**
- `try / except / else / finally` blocks
- Raising custom exceptions: `raise ValueError("message")`
- Creating your own exception classes by inheriting from `Exception`
- Context managers (`with open(...) as f:`) for file safety

**Key idea:** Every place you read a file, parse a value, or do something that *could* fail — wrap it.

---

### 1.4 File I/O

**What it is:** Reading and writing files in Python.

**Why you need it:** You must read the config file and write the output maze file.

**Concepts to learn:**
- `open()` with context manager
- Reading line by line
- Writing strings with `\n`
- Stripping whitespace from lines

---

### 1.5 2D Grids (Lists of Lists)

**What it is:** Representing a grid as `grid[row][col]` where each cell stores a value.

**Why you need it:** The maze is a grid. Each cell stores an integer (0–15) encoding its walls.

**Concept — Wall encoding:**
Each cell's walls are stored as bits in a single integer:
```
Bit 0 (value 1) = North wall
Bit 1 (value 2) = East wall
Bit 2 (value 4) = South wall
Bit 3 (value 8) = West wall
```

So if a cell has North + East walls closed: `1 + 2 = 3` → hex digit `3`
If a cell has all 4 walls: `1+2+4+8 = 15` → hex digit `F`

**Bitwise operations you need to know:**
- Set a bit: `cell |= (1 << bit_index)`
- Check a bit: `if cell & (1 << bit_index):`
- Clear a bit: `cell &= ~(1 << bit_index)`

---

### 1.6 BFS (Breadth-First Search)

**What it is:** An algorithm that explores a graph level by level, guaranteeing the shortest path.

**Why you need it:** You must find the **shortest path** from entry to exit and write it in the output file as a string of N/E/S/W moves.

**How BFS works conceptually:**
1. Start at the entry cell, add it to a queue
2. Pop the first cell from the queue
3. For each neighbor reachable from this cell (no wall blocking), add it to the queue if not visited
4. Track "how did I get here?" using a parent dictionary
5. When you reach the exit, backtrack using the parent dictionary to reconstruct the path

**Key data structures:**
- `collections.deque` as the queue (fast pop from left)
- A `dict` or 2D array to track visited cells and their parent

---

### 1.7 Random Module & Seeds

**What it is:** Python's `random` module for generating random numbers, with a seed for reproducibility.

**Why you need it:** The maze must be randomly generated, but the same seed must always produce the same maze.

**Key functions:**
- `random.seed(value)` — set the seed
- `random.shuffle(list)` — randomly reorder a list in place
- `random.choice(list)` — pick a random element
- `random.randint(a, b)` — pick a random integer between a and b inclusive

---

### 1.8 argparse (Command-line arguments)

**What it is:** The standard Python module for parsing command-line arguments.

**Why you need it:** Your program runs as `python3 a_maze_ing.py config.txt` — you need to extract `config.txt` from `sys.argv` or use `argparse`.

---

## Phase 2 — Understanding Maze Theory

### 2.1 What Is a "Perfect" Maze?

A **perfect maze** has exactly **one path** between any two cells. There are no loops, no isolated regions.

Mathematically, it corresponds to a **spanning tree** of the grid graph — a tree that connects all nodes with no cycles.

If `PERFECT=False`, you can have multiple paths (loops exist), making it easier to get lost.

---

### 2.2 Maze Generation Algorithms

You must choose one algorithm. Here are the main candidates:

#### Recursive Backtracker (DFS)
**How it works:**
1. Start at a random cell, mark it visited
2. Pick a random unvisited neighbor
3. Remove the wall between current cell and that neighbor
4. Move to that neighbor and repeat
5. If no unvisited neighbors exist, backtrack to the previous cell
6. Stop when all cells are visited

**Properties:**
- Generates a perfect maze (spanning tree)
- Tends to create long winding corridors
- Easy to implement with a stack (or recursion)
- Fast

**Recommended for this project** — straightforward and produces nice-looking mazes.

#### Prim's Algorithm
**How it works:**
1. Start with a single cell in the "maze"
2. Maintain a list of "frontier" walls (walls between maze cells and non-maze cells)
3. Pick a random frontier wall, if the cell on the other side is not yet in the maze: add it, remove the wall
4. Add that cell's frontier walls to the list
5. Repeat until all cells are in the maze

**Properties:**
- Also generates a perfect maze
- Tends to create mazes with many short branches, more "tree-like"

#### Kruskal's Algorithm
**How it works:**
1. List all walls in the grid
2. Shuffle them randomly
3. For each wall, if the two cells on either side are not connected (use Union-Find), remove the wall and merge the two sets
4. Continue until all cells are connected

**Properties:**
- Perfect maze
- Requires Union-Find data structure
- Produces mazes with more uniform texture

---

### 2.3 Wall Coherence

**Critical rule from the subject:** If cell A has an East wall, then cell B (to the right of A) MUST also have a West wall. They share that wall.

When you remove a wall during generation, you must remove it from **both** cells.

Example:
```
Cell at (x=0, y=0) has East wall removed → clear bit 1
Cell at (x=1, y=0) must also have West wall removed → clear bit 3
```

---

### 2.4 The "42" Pattern

This is a unique requirement. You must make certain cells **fully closed** (all 4 walls = `F` in hex) arranged to spell "42" when the maze is displayed visually.

**How to approach it:**
- Design pixel-art templates for the digits "4" and "2" on a grid
- Before or after generation, force those cells to have all 4 walls set (`cell = 0xF`)
- Also force neighboring cells to agree (coherence rule)
- These cells are isolated — that's allowed by the subject as an exception to the connectivity rule
- If the maze is too small to fit the pattern, print an error message and skip it

**Minimum size for "42":** You'll need to experiment. A reasonable minimum is around 15×15. The digits need space (roughly 3×5 pixels each, plus spacing).

---

### 2.5 Preventing Open Areas (No 3×3 or Larger)

The subject says corridors can't be wider than 2 cells. This means there can never be a 3×3 block of cells where all interior walls between them are removed.

**How to handle this:** After generation, scan the grid for any 3×3 region where all internal walls are missing. Add walls to break it up. OR enforce this constraint during generation by refusing to remove a wall if it would create such an open area.

---

## Phase 3 — Project Architecture

Plan your files before you code. A clean structure makes the project easier to build, test, and package.

### Recommended File Structure

```
a-maze-ing/
│
├── a_maze_ing.py          ← Main entry point (CLI)
├── config.txt             ← Default config file
├── Makefile               ← Required by subject
├── README.md              ← Required by subject
├── .gitignore             ← Exclude __pycache__, .mypy_cache, venv/
│
├── mazegen/               ← Reusable module (for packaging)
│   ├── __init__.py
│   └── generator.py       ← MazeGenerator class lives here
│
├── display/               ← Visual rendering code
│   └── renderer.py        ← Terminal ASCII renderer
│
├── pyproject.toml         ← Package build config (for pip)
│
└── tests/                 ← Unit tests (not submitted but recommended)
    └── test_generator.py
```

---

### Module Responsibilities

| File | What it does |
|------|-------------|
| `a_maze_ing.py` | Parse args, read config, call MazeGenerator, write output, call display |
| `mazegen/generator.py` | MazeGenerator class: generate maze, solve it, export data |
| `display/renderer.py` | Take a maze grid and draw it in terminal |
| `config.txt` | Default KEY=VALUE configuration |
| `Makefile` | Automate install, run, lint, debug, clean |

---

## Phase 4 — Step-by-Step Implementation Plan

Work through these steps in order. **Do not skip ahead.**

---

### Step 1 — Config File Parser

**Goal:** Read `config.txt` and return a dictionary of settings.

**What to implement:**
- Open the file with a context manager
- Skip lines starting with `#`
- Split each line on `=` to get key and value
- Validate that all required keys exist: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`
- Validate types: WIDTH and HEIGHT must be positive integers, ENTRY/EXIT must be valid coordinates inside the grid
- Raise clear errors for anything invalid

**Test it:** Try giving it a bad file, a missing key, a negative width — make sure it never crashes silently.

---

### Step 2 — Grid Initialization

**Goal:** Create the maze grid as a 2D list.

**What to implement:**
- Create a `list[list[int]]` of size `height × width`
- Initialize every cell with all 4 walls closed: value `15` (binary `1111`)
- This represents a fully walled grid — generation will open walls

**Concept:** Starting with all walls and removing them (as in DFS/Prim's) is cleaner than starting empty and adding walls.

---

### Step 3 — Maze Generation (Recursive Backtracker recommended)

**Goal:** Implement the DFS recursive backtracker.

**What to implement:**
- A `generate()` method in your `MazeGenerator` class
- Use a stack (list) instead of actual recursion to avoid Python's recursion limit on large mazes
- Track visited cells
- When removing a wall between two cells, update **both** cells (coherence)
- Respect the seed: call `random.seed(seed)` before generation

**Direction mapping you'll need:**
```
N → row - 1, col + 0  → bit 0 in current, bit 2 in neighbor
E → row + 0, col + 1  → bit 1 in current, bit 3 in neighbor
S → row + 1, col + 0  → bit 2 in current, bit 0 in neighbor
W → row + 0, col - 1  → bit 3 in current, bit 1 in neighbor
```

**After generation:** Verify that ENTRY and EXIT cells have their outer border walls properly set (they are inside the maze — they shouldn't have openings to outside by default, unless you explicitly carve entry/exit points).

---

### Step 4 — Enforce Outer Borders

**Goal:** All cells on the border of the maze must have their outermost wall closed.

**What to implement:**
- Top row: all cells must have North wall set
- Bottom row: all cells must have South wall set
- Left column: all cells must have West wall set
- Right column: all cells must have East wall set

**Why:** The subject says "there must be walls at external borders."

---

### Step 5 — Embed the "42" Pattern

**Goal:** Force a set of cells to be fully closed (value `F`) to visually spell "42."

**What to implement:**
- Design pixel maps for "4" and "2" (suggest 3 wide × 5 tall each, with 1 column spacing)
- Pick a location in the maze to place them (center, bottom-right, etc.)
- For each cell in the pattern, set its value to `15` (all walls closed)
- Also update all neighbors of those cells to agree on the shared walls
- Check if the maze is large enough; if not, print an error and skip

**Pixel art approach:** Think of each digit as a 3×5 or 4×6 boolean grid. `True` = wall cell (fully closed), `False` = normal maze cell.

---

### Step 6 — Prevent 3×3 Open Areas

**Goal:** Scan the grid and add walls to eliminate any 3×3 completely open region.

**What to implement:**
- Iterate over every possible 3×3 starting position
- Check if all 4 internal walls in that region are open (between the 9 cells)
- If so, add at least one internal wall to break the open area
- Remember to maintain coherence when adding walls

---

### Step 7 — BFS Solver

**Goal:** Find the shortest path from ENTRY to EXIT.

**What to implement:**
- A `solve()` method that returns a list of moves (e.g., `['S', 'S', 'E', 'N', ...]`)
- Use BFS with a `deque` for the queue
- For each cell, try all 4 directions — only move if the wall in that direction is open
- Track parents to reconstruct the path
- Return `None` or raise an error if no path exists (shouldn't happen in a valid maze)

---

### Step 8 — Output File Writer

**Goal:** Write the maze to a file in the specified format.

**Format recap:**
- One row per line, each cell as one hex character (0–F)
- Empty line
- Entry coordinates (e.g., `0,0`)
- Exit coordinates (e.g., `19,14`)
- Shortest path as a string of N/E/S/W (e.g., `SSEENNEESS...`)
- Every line ends with `\n`

**What to implement:**
- Loop over rows, join hex values, write line
- Write blank line
- Write entry, exit, path

---

### Step 9 — Perfect Maze Verification (optional but good practice)

If `PERFECT=True`, verify your maze actually is perfect by checking that BFS can reach every cell from the entry, and that there's exactly one path. If not, something is wrong with your generation.

---

## Phase 5 — Visual Representation

### 5.1 Terminal ASCII Rendering

**Goal:** Draw the maze in the terminal using characters and ANSI color codes.

**How to approach it:**

Each maze cell is drawn as a block of characters. A common approach uses a **3×3 character block per cell:**

```
+--+
|  |
+--+
```

But a cleaner approach uses a **top-left corner** drawing method, where you draw walls only at the top and left of each cell (avoids double-drawing shared walls).

**ANSI color codes:** These are escape sequences printed directly to the terminal:
```
\033[31m  → Red text
\033[42m  → Green background
\033[0m   → Reset
```

Use these to colorize: walls, the path, entry (green/magenta), exit (red), "42" pattern cells.

**Menu system:**
After drawing, display a menu:
```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Quit
Choice (1-4):
```
Read input with `input()` and loop.

---

### 5.2 User Interactions to Implement

| Action | What happens |
|--------|-------------|
| Re-generate | Call `MazeGenerator` again with a new or same seed, redraw |
| Show/Hide path | Toggle a flag; redraw with or without path highlighted |
| Change wall color | Cycle through a list of ANSI color codes for walls |
| Quit | Exit the loop cleanly |

---

### 5.3 Drawing Algorithm (Recommended Approach)

Render the maze into a 2D character grid of size `(2*height+1) × (2*width+1)`:
- Odd rows/cols = cell interiors
- Even rows/cols = walls between cells or outer border

This approach cleanly separates "is this a wall?" from "is this a cell?"

---

## Phase 6 — Reusable Package (mazegen)

### 6.1 What Must Be Packaged

The `MazeGenerator` class and its logic must live in a standalone module that can be installed with pip independently of your main project.

---

### 6.2 Python Packaging Concepts

**`pyproject.toml`** — Modern Python packaging config file. Replaces `setup.py`.

Minimum structure:
```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "mazegen-yourlogin"
version = "1.0.0"
requires-python = ">=3.10"
```

**Building the package:**
```bash
pip install build
python -m build
```
This creates a `dist/` folder containing `.whl` and `.tar.gz` files.

**Installing locally for testing:**
```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

---

### 6.3 `MazeGenerator` Class API (Design It Yourself)

Think about what interface you want to expose. At minimum:

```
MazeGenerator(width, height, seed=None, perfect=True)
    .generate()         → builds the maze
    .grid               → the 2D wall data
    .solve(entry, exit) → returns path as list of directions
    .entry              → (x, y) tuple
    .exit               → (x, y) tuple
```

The class should NOT depend on the visual display code. Keep it pure data logic.

---

### 6.4 Documentation for the Package

Write a docstring at the top of `generator.py` and include a usage example. This should also appear in your README.

Minimum doc sections:
- How to install
- How to instantiate
- How to pass custom parameters
- How to access the grid
- How to get the solution
- A basic code example

---

## Phase 7 — Bonus Features

### Bonus 1 — Multiple Algorithms

**Goal:** Support at least 2 algorithms selectable via config (e.g., `ALGORITHM=dfs` or `ALGORITHM=prim`).

**How to implement:**
- Add an `ALGORITHM` key to your config parser
- Create separate methods or classes for each algorithm
- Use a factory pattern: based on the config value, instantiate the right algorithm

**Prim's algorithm concepts to learn:**
- Maintaining a frontier list
- Randomly selecting from the frontier
- Union-Find is not required for Prim's (unlike Kruskal's)

---

### Bonus 2 — Generation Animation

**Goal:** Show the maze being built step by step in the terminal.

**How to implement:**
- After each wall removal in your generation algorithm, redraw the current state
- Use ANSI escape codes to clear the screen: `\033[H\033[J` or `os.system('clear')`
- Add a small delay with `time.sleep(0.05)` between frames
- Optionally show the current cell being processed in a different color

**Key concept — generator functions (`yield`):**
Instead of running the whole generation at once, use `yield` to pause after each step. Your main loop can then call `next()` to advance one step at a time.

```python
# Concept — not the actual implementation
def generate_step_by_step(self):
    # ... setup ...
    while stack:
        # ... one step of DFS ...
        yield self.grid  # pause and return current state
```

---

## Phase 8 — README & Submission Checklist

### README.md Required Sections

- [ ] First line: *This project has been created as part of the 42 curriculum by \<login\>.*
- [ ] Description section
- [ ] Instructions section (how to install and run)
- [ ] Resources section (links + how you used AI)
- [ ] Complete config file format (all keys, types, examples)
- [ ] Which algorithm you chose and WHY
- [ ] What part of your code is reusable and how to use it
- [ ] Team management (roles, planning, what worked, tools used)
- [ ] mazegen package usage documentation

---

### Final Submission Checklist

#### Code
- [ ] Main file is named `a_maze_ing.py`
- [ ] Runs with `python3 a_maze_ing.py config.txt`
- [ ] Never crashes — all errors handled gracefully
- [ ] Type hints on all functions and variables
- [ ] Passes `mypy` without errors
- [ ] Passes `flake8` (PEP 8 compliance)
- [ ] All functions have docstrings (Google or NumPy style)

#### Maze Correctness
- [ ] Width and height respected
- [ ] Entry and exit are valid and different
- [ ] All cells reachable (full connectivity)
- [ ] Outer borders have walls
- [ ] Wall coherence (shared walls match between neighbors)
- [ ] No 3×3 open areas
- [ ] "42" pattern visible (or error message if too small)
- [ ] PERFECT mode: exactly one path between entry and exit

#### Output File
- [ ] One hex digit per cell
- [ ] One row per line
- [ ] Empty line after grid
- [ ] Entry coordinates on next line
- [ ] Exit coordinates on next line
- [ ] Shortest path (N/E/S/W) on last line
- [ ] All lines end with `\n`

#### Visual Display
- [ ] Shows walls, entry, exit
- [ ] Menu with at least 4 options
- [ ] Re-generate works
- [ ] Show/Hide path works
- [ ] Color change works

#### Package
- [ ] `mazegen-*.whl` or `mazegen-*.tar.gz` at root of repo
- [ ] `pyproject.toml` (or equivalent) present to rebuild from source
- [ ] Can be installed with `pip install`
- [ ] MazeGenerator class works after installation

#### Makefile Rules
- [ ] `make install`
- [ ] `make run`
- [ ] `make debug`
- [ ] `make clean`
- [ ] `make lint` (runs flake8 and mypy with required flags)

#### Repository
- [ ] Default `config.txt` present
- [ ] `.gitignore` excludes `__pycache__`, `.mypy_cache`, `venv/`, `dist/`
- [ ] `README.md` complete

---

## Concepts Quick Reference

### Bit Operations for Walls

| Direction | Bit | Value | Check | Set | Clear |
|-----------|-----|-------|-------|-----|-------|
| North | 0 | 1 | `cell & 1` | `cell \|= 1` | `cell &= ~1` |
| East | 1 | 2 | `cell & 2` | `cell \|= 2` | `cell &= ~2` |
| South | 2 | 4 | `cell & 4` | `cell \|= 4` | `cell &= ~4` |
| West | 3 | 8 | `cell & 8` | `cell \|= 8` | `cell &= ~8` |

**All walls closed:** `15` (hex `F`)
**No walls:** `0`

---

### Direction Vectors

```
N: (row-1, col+0)  → opposite is S
E: (row+0, col+1)  → opposite is W
S: (row+1, col+0)  → opposite is N
W: (row+0, col-1)  → opposite is E
```

When removing wall between cell A and neighbor B:
- Remove direction bit from A
- Remove **opposite** direction bit from B

---

### Algorithm Comparison

| Algorithm | Pattern | Complexity | Difficulty |
|-----------|---------|------------|------------|
| Recursive Backtracker | Long corridors | O(n) | Easy |
| Prim's | Many branches, organic | O(n log n) | Medium |
| Kruskal's | Uniform texture | O(n log n) | Medium (needs Union-Find) |

---

### ANSI Color Code Quick Reference

```
\033[0m    Reset
\033[1m    Bold
\033[30m   Black text
\033[37m   White text
\033[31m   Red text
\033[32m   Green text
\033[33m   Yellow text
\033[34m   Blue text
\033[41m   Red background
\033[42m   Green background
\033[43m   Yellow background
\033[44m   Blue background
\033[40m   Black background
```

---

### BFS Template (Conceptual)

```
queue = deque([(start_row, start_col)])
visited = {(start_row, start_col): None}  # maps cell → parent cell

while queue:
    current = queue.popleft()
    if current == exit:
        break
    for each direction:
        if wall in that direction is OPEN:
            neighbor = cell in that direction
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)

# Reconstruct path by backtracking through visited
```

---

### Config File Format

```
# This is a comment
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=dfs
```

---

## Learning Resources

### Must-Read
- [Python `typing` module docs](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [Python `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque)
- [Python `random` module](https://docs.python.org/3/library/random.html)

### Maze Algorithms
- [Jamis Buck's Maze Generation blog](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap) — the best visual explanations of all maze algorithms
- [Think Labyrinth — Maze algorithms](https://www.astrolog.org/labyrnth/algrithm.htm)
- [Wikipedia — Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

### Python Packaging
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)
- [pyproject.toml reference](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

### ANSI Terminal Colors
- [ANSI escape codes reference](https://en.wikipedia.org/wiki/ANSI_escape_code)

---

*Last updated for A-Maze-ing v2.0*
