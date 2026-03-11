#!/usr/bin/env python3
import random
from renderer import renderer
from globals import PATTERN_2, PATTERN_4, OPPOSITE, DIRECTION


class MazeGenerator:
    def __init__(
        self, width: int, height: int, seed: int | None = None
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 999999)
        self.grid: list[list[int]] = [[0xF] * width for _ in range(height)]
        self.locked: set = set()

    def _stamp_42(self) -> None:
        pattern_w = 5
        pattern_h = 7
        gap = 1
        total_w = pattern_w * 2 + gap

        if self.width < total_w + 2 or self.height < pattern_h + 2:
            print("Maze too small to display '42' pattern.")
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
        return 0 <= x < self.width and 0 <= y < self.height

    def _remove_wall(
        self, x1: int, y1: int, x2: int, y2: int, direction: int
    ) -> None:
        self.grid[y1][x1] &= ~direction
        self.grid[y2][x2] &= ~OPPOSITE[direction]

    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: set
    ) -> list[tuple[int, int, int]]:
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
    renderer(mg.grid, mg.width, mg.height, mg.locked)
