#!/usr/bin/env python3
import random
from typing import List, Tuple, Optional
from renderer import renderer

# Gruvbox colors (ANSI escape codes)
# [*ANSI = a standard for colors in the terminal*]
RESET = "\033[0m"
WALL = "\033[38;2;40;40;40m\033[48;2;40;40;40m"  # dark background
CELL = "\033[48;2;50;48;47m"  # gruvbox bg
LOCKED = "\033[38;2;251;73;52m\033[48;2;251;73;52m"  # gruvbox red for "42"
PATH = "\033[48;2;184;187;38m"  # gruvbox yellow

# Wall bits
NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

DIRECTION = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}

PATTERN_4 = [
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
]

PATTERN_2 = [
    [1, 1, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0],
]


class MazeGenerator:
    def __init__(
        self, width: int, height: int, seed: Optional[int] = None
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 999999)
        self.grid: List[List[int]] = [[0xF] * width for _ in range(height)]
        self.locked: set = set()

    def _stamp_42(self) -> None:
        pattern_w = 5
        pattern_h = 7
        gap = 1
        total_w = pattern_w * 2 + gap

        if self.width < total_w + 2 or self.height < pattern_h + 2:
            print("Maze too small to display '42' pattern.")
            return

        start_x = (self.width - total_w) // 2
        start_y = (self.height - pattern_h) // 2

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
        return 0 <= x < self.width and 0 <= y < self.height

    def _remove_wall(
        self, x1: int, y1: int, x2: int, y2: int, direction: int
    ) -> None:
        self.grid[y1][x1] &= ~direction
        self.grid[y2][x2] &= ~OPPOSITE[direction]

    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: set
    ) -> List[Tuple[int, int, int]]:
        neighbors = []
        for direction, (dx, dy) in DIRECTION.items():
            nx, ny = x + dx, y + dy
            if (
                self._in_bounds(nx, ny)
                and (nx, ny) not in visited
                and (nx, ny) not in self.locked
            ):
                neighbors.append((nx, ny, direction))
        return neighbors

    def generate(self) -> None:
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
    mg = MazeGenerator(30, 20)
    mg.generate()
    render(mg.grid, mg.width, mg.height, mg.locked)
