#!/usr/bin/env python3
import sys
import random
import globals
from solver import bfs
from renderer import renderer
from globals import PATTERN_2, PATTERN_4, OPPOSITE, DIRECTION


class MazeGenerator:
    def __init__(
        self, width: int, height: int, seed: int | None = None
    ) -> None:
        """Initialize the maze generator.

        Args:
            width: Number of columns.
            height: Number of rows.
            seed: Random seed for reproducibility.
        """
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 999999)
        self.grid: list[list[int]] = [[0xF] * width for _ in range(height)]
        self.locked: set = set()

    def _stamp_42(self) -> None:
        """Stamp the 42 pattern into the maze as fully closed cells."""
        pattern_w = 3
        pattern_h = 5
        gap = 1
        total_w = pattern_w * 2 + gap

        if self.width < total_w + 2 or self.height < pattern_h + 2:
            print("Maze too small to display 42 pattern.")
            return

        start_x: int = (self.width - total_w) // 2
        start_y: int = (self.height - pattern_h) // 2

        for row in range(pattern_h):
            for col in range(pattern_w):
                if PATTERN_4[row][col]:
                    cx = start_x + col
                    cy = start_y + row
                    self.grid[cy][cx] = 0xF
                    self.locked.add((cx, cy))
                if PATTERN_2[row][col]:
                    cx = start_x + pattern_w + gap + col
                    cy = start_y + row
                    self.grid[cy][cx] = 0xF
                    self.locked.add((cx, cy))

    def _in_bounds(self, x: int, y: int) -> bool:
        """Check if (x, y) is inside the maze.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            True if inside bounds.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def _remove_wall(
        self, x1: int, y1: int, x2: int, y2: int, direction: int
    ) -> None:
        """Remove wall between two adjacent cells.

        Args:
            x1: Column of first cell.
            y1: Row of first cell.
            x2: Column of second cell.
            y2: Row of second cell.
            direction: Wall bit to remove.
        """
        self.grid[y1][x1] &= ~direction
        self.grid[y2][x2] &= ~OPPOSITE[direction]

    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: set
    ) -> list[tuple[int, int, int]]:
        """Get unvisited neighbors of a cell.

        Args:
            x: Current x position.
            y: Current y position.
            visited: Set of already visited (x, y) cells.

        Returns:
            List of (nx, ny, wall_bit) tuples.
        """
        neighbors = []
        for letter, (dx, dy, wall_bit) in DIRECTION.items():
            nx, ny = x + dx, y + dy
            if (
                self._in_bounds(nx, ny)
                and (nx, ny) not in visited
                and (nx, ny) not in self.locked
            ):
                neighbors.append((nx, ny, wall_bit))
        return neighbors

    def generate(self) -> None:
        """Generate the maze using recursive backtracker (DFS)."""
        random.seed(self.seed)
        self._stamp_42()

        start = (0, 0)
        while start in self.locked:
            start = (start[0] + 1, start[1])

        visited = {start} | self.locked
        stack = [start]

        while stack:
            x, y = stack[-1]
            neighbors = self._get_unvisited_neighbors(x, y, visited)

            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                self._remove_wall(x, y, nx, ny, direction)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()


if __name__ == "__main__":
    from parser_config import parse_config, validate_config

    # --- read config file ---
    if len(sys.argv) != 2:
        print("Usage: python3 generator.py config.txt")
        sys.exit(1)

    try:
        raw = parse_config(sys.argv[1])
        config = validate_config(raw)
    except Exception as e:
        print(f"Config error: {e}")
        sys.exit(1)

    width = config["WIDTH"]
    height = config["HEIGHT"]
    seed = config.get("SEED")
    entry = (config["ENTRY"].x, config["ENTRY"].y)
    exit_ = (config["EXIT"].x,  config["EXIT"].y)
    outfile = config["OUTPUT_FILE"]

    # --- generate maze ---
    mg = MazeGenerator(width, height, seed)
    mg.generate()

    # --- solve ---
    result = bfs(mg.grid, entry, exit_)
    if result is None:
        print("Error: no path found")
        sys.exit(1)
    path_cells, direction_str = result

    # --- write output file ---
    try:
        with open(outfile, 'w') as f:
            for row in mg.grid:
                f.write(''.join(format(cell, 'X') for cell in row) + '\n')
            f.write('\n')
            f.write(f'{entry[0]},{entry[1]}\n')
            f.write(f'{exit_[0]},{exit_[1]}\n')
            f.write(direction_str + '\n')
    except OSError as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    # BUG 1 — show_path was used before being defined
    show_path: bool = False

    # wall colors list for option 3
    wall_colors: list[str] = [
        "\033[38;2;60;56;54m\033[48;2;28;28;28m",    # dark (default)
        "\033[38;2;7;102;120m\033[48;2;7;102;120m",  # teal
        "\033[38;2;100;60;20m\033[48;2;100;60;20m",  # brown
        "\033[38;2;60;60;100m\033[48;2;60;60;100m",  # blue-grey
    ]

    # --- menu loop ---
    while True:

        renderer(
            mg.grid,
            mg.width,
            mg.height,
            mg.locked,
            path_cells if show_path else None,
            entry,
            exit_,
        )

        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = input("Choice (1-4): ").strip()

        if choice == "1":
            # BUG 2 — was calling old solve() and path_to_directions()
            mg = MazeGenerator(width, height)
            mg.generate()
            result = bfs(mg.grid, entry, exit_)
            if result is not None:
                path_cells, direction_str = result
            else:
                path_cells, direction_str = [], ""
            show_path = False

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            # BUG 3 — renderer imports WALL as a copy so we must
            # use globals.WALL directly and re-import each render
            try:
                idx = wall_colors.index(globals.WALL)
            except ValueError:
                idx = 0
            globals.WALL = wall_colors[(idx + 1) % len(wall_colors)]

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice — enter 1, 2, 3 or 4")
