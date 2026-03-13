from collections import deque
from .constants import NORTH, EAST, SOUTH, WEST

# For the seek of path finding
PATH_DIRECTION = {
    'N': (0, -1, NORTH),
    'E': (1, 0, EAST),
    'S': (0, 1, SOUTH),
    'W': (-1, 0, WEST),
}

def maze_solver(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> tuple[list[tuple[int, int]], str] | None:
    """Find shortest path, return both cell list and direction string.

    Args:
        grid: The maze grid as grid[y][x].
        entry: Start position as (x, y).
        exit_: End position as (x, y).

    Returns:
        Tuple of (cell_list, direction_string) or None if no path.
    """
    start = entry
    goal = exit_
    rows = len(grid)
    cols = len(grid[0])

    queue: deque[tuple] = deque()
    # store (x, y, cell_path, direction_path) together
    queue.append((start[0], start[1], [start], ""))

    visited: set[tuple[int, int]] = {start}

    while queue:
        x, y, cell_path, dir_path = queue.popleft()

        if (x, y) == goal:
            return cell_path, dir_path   # return BOTH

        for letter, (dx, dy, wall_bit) in PATH_DIRECTION.items():

            if grid[y][x] & wall_bit:
                continue

            nx = x + dx
            ny = y + dy

            if not (0 <= nx < cols and 0 <= ny < rows):
                continue

            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            queue.append((
                nx,
                ny,
                cell_path + [(nx, ny)],   # add cell to cell path
                dir_path + letter,        # add letter to direction path
            ))

    return None