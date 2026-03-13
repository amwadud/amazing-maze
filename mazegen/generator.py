#!/usr/bin/env python3
"""Maze generator using iterative DFS (recursive backtracker algorithm)."""

import random

from .constants import NORTH, EAST, SOUTH, WEST, OPPOSITE, DIRECTION
from .constants import PATTERN_4, PATTERN_2


class MazeGenerator:
    """Maze generator using iterative DFS (recursive backtracker).

    Quick start:
        mg = MazeGenerator(20, 15, seed=42, perfect=True)
        mg.generate()
        # mg.grid   — 2-D list[list[int]], each cell is a 4-bit wall bitmask
        # mg.locked — set of (x, y) cells belonging to the "42" pattern
    """

    def __init__(
        self, width: int, height: int, seed: int | None = None, perfect: bool = True
    ) -> None:
        """Args:
            width:   Number of columns (>= 3).
            height:  Number of rows    (>= 3).
            seed:    RNG seed for reproducibility. Random if None.
            perfect: True = one path between any two cells (no loops).
        """
        self.width   = width
        self.height  = height
        self.seed    = seed if seed is not None else random.randint(0, 999_999)
        self.perfect = perfect
        self.grid:   list[list[int]]      = [[0xF] * width for _ in range(height)]
        self.locked: set[tuple[int, int]] = set()

    # ── helpers ───────────────────────────────────────────────────────────────

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _remove_wall(self, x1: int, y1: int, x2: int, y2: int, d: int) -> None:
        """Open the wall between (x1,y1) and (x2,y2) in direction d."""
        self.grid[y1][x1] &= ~d
        self.grid[y2][x2] &= ~OPPOSITE[d]

    def _get_neighbors(
        self, x: int, y: int, visited: set[tuple[int, int]]
    ) -> list[tuple[int, int, int]]:
        """Return unvisited, unlocked neighbors as (nx, ny, direction)."""
        return [
            (x + dx, y + dy, d)
            for d, (dx, dy) in DIRECTION.items()
            if self._in_bounds(x + dx, y + dy)
            and (x + dx, y + dy) not in visited
            and (x + dx, y + dy) not in self.locked
        ]

    def _stamp_42(self) -> None:
        """Lock cells forming the '42' pattern at the center of the maze."""
        pw, ph = len(PATTERN_4[0]), len(PATTERN_4)
        total  = pw * 2

        if self.width < total + 2 or self.height < ph + 2:
            print("Warning: maze too small for '42' pattern — skipped.")
            return

        sx = (self.width  - total) // 2
        sy = (self.height - ph)    // 2

        for row in range(ph):
            for col in range(pw):
                if PATTERN_4[row][col]:
                    self.locked.add((sx + col,      sy + row))
                if PATTERN_2[row][col]:
                    self.locked.add((sx + pw + col, sy + row))

    def _add_loops(self, ratio: float = 0.1) -> None:
        """Remove ~ratio% of remaining walls to create shortcuts."""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.locked:
                    continue
                for d, (dx, dy) in DIRECTION.items():
                    nx, ny = x + dx, y + dy
                    if (
                        self._in_bounds(nx, ny)
                        and (nx, ny) not in self.locked
                        and self.grid[y][x] & d
                        and random.random() < ratio
                    ):
                        self._remove_wall(x, y, nx, ny, d)

    # ── public API ────────────────────────────────────────────────────────────

    def generate(self) -> None:
        """Generate the maze in-place using iterative DFS."""
        random.seed(self.seed)
        self._stamp_42()

        visited: set[tuple[int, int]] = {(0, 0)} | self.locked
        stack:   list[tuple[int, int]] = [(0, 0)]

        while stack:
            x, y = stack[-1]
            neighbors = self._get_neighbors(x, y, visited)
            if neighbors:
                nx, ny, d = random.choice(neighbors)
                self._remove_wall(x, y, nx, ny, d)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        # Locked cells must stay fully walled — restore any accidental carves.
        for cx, cy in self.locked:
            self.grid[cy][cx] = 0xF

        if not self.perfect:
            self._add_loops()


if __name__ == "__main__":
    width = int(input("Enter width for the maze: "))
    height = int(input("Enter height for the maze: "))
    mg = MazeGenerator(width, height)
    mg.generate()
    render(mg.grid, mg.width, mg.height, locked=mg.locked)
