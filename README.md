*This project has been created as part of the 42 curriculum by abait-el, hlaaz.*

# A-Maze-ing

A Python maze generator that creates random mazes from a configuration file, displays them visually in the terminal, and exports the maze data in hexadecimal format.

## Description

A-Maze-ing generates random mazes using the **recursive backtracker algorithm** (iterative depth-first search). The generator can produce:
- **Perfect mazes**: Exactly one path between any two cells (no loops)
- **Non-perfect mazes**: With additional passages for shortcuts/loops

The maze is encoded as hexadecimal digits where each cell's 4 bits represent walls (North, East, South, West). A special "42" pattern is stamped into the maze using fully locked cells at the center.

### Key Features

- Configurable maze dimensions and entry/exit points
- Reproducible generation via seed
- Shortest path solving (BFS)
- Terminal-based visual rendering with multiple color themes
- TUI interactions: regenerate, toggle path, change themes, quit
- Hexadecimal output file format

## Instructions

### Installation

```bash
make install
```

or

```bash
pip install -r requirements.txt
```

### Running the Program

```bash
make run
```

or

```bash
python3 a_maze_ing.py config.txt
```

### Debug Mode

```bash
make debug
```

### Cleaning

```bash
make clean
```

### Linting

```bash
make lint
```

Strict mode:

```bash
make lint-strict
```

## Configuration File Format

The program reads settings from a configuration file (default: `config.txt`).

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Number of columns (>= 3) | `WIDTH=20` |
| `HEIGHT` | Number of rows (>= 3) | `HEIGHT=18` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=9,9` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze (True/False) | `PERFECT=True` |
| `SEED` | Random seed (optional) | `SEED=1337` |

Lines starting with `#` are comments.

Example configuration:
```
# A-Maze-ing default configuration
WIDTH=20
HEIGHT=18
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=1337
```

## Maze Generation Algorithm

**Recursive Backtracker (Iterative DFS)**

The algorithm works as follows:
1. Start with a grid where all cells are fully walled
2. Pick a starting cell (entry point), mark as visited
3. While there are unvisited cells:
   - If current cell has unvisited neighbors, pick one at random
   - Remove the wall between current and chosen cell
   - Move to chosen cell and push to stack
   - Otherwise, backtrack (pop from stack)
4. For non-perfect mazes, randomly remove ~10% of remaining walls to create loops

This produces a perfect maze with exactly one path between any two cells.

**Why Recursive Backtracker?**
- Simple to implement and understand
- Produces long, winding corridors ideal for mazes
- Efficient O(width × height) time complexity
- Naturally creates a spanning tree structure

## Code Reusability

The maze generation logic is encapsulated in the `mazegen` module, which can be imported into future projects.

### Basic Usage

```python
from mazegen import MazeGenerator

# Create and generate a maze
mg = MazeGenerator(width=20, height=15, seed=42, perfect=True)
mg.generate()

# Access the generated structure
print(mg.grid)   # 2D list of wall bitmasks
print(mg.locked) # Set of "42" pattern cells

# Find shortest path
from mazegen import maze_solver
path, directions = maze_solver(mg.grid, (0, 0), (19, 14))
print(f"Path: {directions}")  # e.g., "ESWN..."
```

### MazeGenerator Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | int | Number of columns (>= 3) |
| `height` | int | Number of rows (>= 3) |
| `seed` | int \| None | RNG seed for reproducibility |
| `perfect` | bool | If True, creates loopless maze |

### MazeGenerator Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `grid` | list[list[int]] | 2D maze; each cell is a 4-bit wall bitmask |
| `locked` | set[tuple[int, int]] | Cells belonging to the "42" pattern |
| `width` | int | Maze width |
| `height` | int | Maze height |

### Wall Bitmask Reference

| Bit | Direction |
|-----|-----------|
| 1 (0b0001) | North |
| 2 (0b0010) | East |
| 4 (0b0100) | South |
| 8 (0b1000) | West |

Example: `0x5` (binary 0101) = North and South walls open, East and West closed.

## Team & Project Management

### Roles

- **abait-el**: Implementation
- **hlaaz**: Implementation

### Tools Used

- Python 3.10+
- flake8 for linting
- mypy for type checking
- pdb for debugging

## Resources

- [Recursive Backtracker Algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)
- [Maze Generation - Jamis Buck](https://weblog.jamisbuck.org/under construction)
- [Spanning Trees & Perfect Mazes](https://en.wikipedia.org/wiki/Spanning_tree)
- [42 Intra Project Page](https://cdn.intra.42.fr/pdf/pdf/201862/en.subject.pdf)

## AI Usage

AI tools were used for:
- Brainstorming the overall architecture
- Understanding maze generation algorithms
- Debugging and code review
- Documentation formatting