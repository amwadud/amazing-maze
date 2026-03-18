#!/usr/bin/env python3
"""Maze generator using iterative DFS (recursive backtracker algorithm)."""

import random
from abc import ABC, abstractmethod
from typing import Any

from .constants import DIRECTION, OPPOSITE, PATTERN_2, PATTERN_4


class MazeGenerator(ABC):
    """Abstract base class for maze generators.

    Quick start:
        # Perfect maze
        from mazegen import PerfectMazeGenerator
        mg = PerfectMazeGenerator(20, 15, seed=42)
        mg.generate()

        # Imperfect maze (with loops)
        from mazegen import ImperfectMazeGenerator
        mg = ImperfectMazeGenerator(20, 15, seed=42)
        mg.generate()

        # Access the generated maze
        # mg.grid   — 2-D list[list[int]], each cell is a 4-bit wall bitmask
        # mg.locked — set of (x, y) cells belonging to the "42" pattern
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
    ) -> None:
        """Args:
        width:   Number of columns (>= 3).
        height:  Number of rows    (>= 3).
        seed:    RNG seed for reproducibility. Random if None.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[int]] = [[0xF] * width for _ in range(height)]
        self.locked: set[tuple[int, int]] = set()

    def _reinit_grid(self) -> None:
        self.grid = [[0xF] * self.width for _ in range(self.height)]

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
        total = pw * 2

        if self.width < total + 2 or self.height < ph + 2:
            print("Warning: maze too small for '42' pattern — skipped.")
            return

        sx = (self.width - total) // 2
        sy = (self.height - ph) // 2

        for row in range(ph):
            for col in range(pw):
                if PATTERN_4[row][col]:
                    self.locked.add((sx + col, sy + row))
                if PATTERN_2[row][col]:
                    self.locked.add((sx + pw + col, sy + row))

    def _run_dfs(self, start: tuple[int, int] = (0, 0)) -> None:
        """Run recursive backtracker algorithm from start position."""
        visited: set[tuple[int, int]] = {start} | self.locked
        stack: list[tuple[int, int]] = [start]

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

        for cx, cy in self.locked:
            self.grid[cy][cx] = 0xF

    @abstractmethod
    def generate(self) -> None:
        """Generate the maze in-place."""
        ...


class PerfectMazeGenerator(MazeGenerator):
    """Generate a perfect maze with exactly one path between any two cells."""

    def generate(self) -> None:
        """Generate a perfect maze (no loops) using iterative DFS."""
        self._reinit_grid()
        random.seed(self.seed)
        self._stamp_42()
        self._run_dfs()


class ImperfectMazeGenerator(MazeGenerator):
    """Generate an imperfect maze with loops/shortcuts."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        loop_ratio: float = 0.1,
    ) -> None:
        """Args:
        width:      Number of columns (>= 3).
        height:    Number of rows    (>= 3).
        seed:      RNG seed for reproducibility. Random if None.
        loop_ratio: Fraction of walls to remove (default 0.1 = 10%).
        """
        super().__init__(width, height, seed)
        self.loop_ratio = loop_ratio

    def _add_loops(self) -> None:
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
                        and random.random() < self.loop_ratio
                    ):
                        self._remove_wall(x, y, nx, ny, d)

    def generate(self) -> None:
        """Generate an imperfect maze (with loops) using iterative DFS."""
        self._reinit_grid()
        random.seed(self.seed)
        self._stamp_42()
        self._run_dfs()
        self._add_loops()


def create_generator(
    width: int,
    height: int,
    seed: int | None = None,
    perfect: bool = True,
    **kwargs: Any,
) -> MazeGenerator:
    """Factory to create the appropriate maze generator.

    Args:
        width:   Number of columns (>= 3).
        height:  Number of rows    (>= 3).
        seed:    RNG seed for reproducibility. Random if None.
        perfect: If True, returns PerfectMazeGenerator.
        **kwargs: Additional arguments passed to the generator.

    Returns:
        PerfectMazeGenerator or ImperfectMazeGenerator instance.
    """
    if perfect:
        return PerfectMazeGenerator(width, height, seed)
    return ImperfectMazeGenerator(width, height, seed, **kwargs)


if __name__ == "__main__":
    width = int(input("Enter width for the maze: "))
    height = int(input("Enter height for the maze: "))
    mg = PerfectMazeGenerator(width, height)
    mg.generate()
    from display import render_tui

    render_tui(mg.grid, mg.width, mg.height, locked=mg.locked)
