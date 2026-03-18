import os
import time

from mazegen.constants import EAST, NORTH, WEST

from display.renderer_tui import render_tui

RESET = "\033[0m"
EMPTY = "  "


def _has(grid, x, y, d):
    """Returns True if cell (x, y) has a wall in direction d."""
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] & d


def _on_path(x, y, path, entry, exit_):
    """Check if cell is entry, exit, or on solution path."""
    return (x, y) in path or (x, y) == entry or (x, y) == exit_


def _gap(x1, y1, x2, y2, path, entry, exit_, theme):
    """Returns colored gap if both cells on path, otherwise empty."""
    if _on_path(x1, y1, path, entry, exit_) and _on_path(
        x2, y2, path, entry, exit_
    ):
        return theme["PATH_COLOR"] + EMPTY + RESET
    return EMPTY


def _cell(x, y, locked, path, entry, exit_, theme):
    """Returns a colored string representing one maze cell."""
    if (x, y) == entry:
        return theme["ENTRY_COLOR"] + " S" + RESET
    if (x, y) == exit_:
        return theme["EXIT_COLOR"] + " E" + RESET
    if (x, y) in locked:
        return theme["LOCKED_COLOR"] + EMPTY + RESET
    if (x, y) in path:
        return theme["PATH_COLOR"] + EMPTY + RESET
    return EMPTY


def animate_solution(
    grid, w, h, locked, path, entry, exit_, theme, delay=0.03
):
    """Animate the solution path being drawn step by step."""
    locked = locked or set()

    for i in range(1, len(path) + 1):
        os.system("clear")
        current_path = set(path[:i])
        render_tui(grid, w, h, locked, current_path, entry, exit_, theme)
        time.sleep(delay)

    os.system("clear")
    render_tui(grid, w, h, locked, set(path), entry, exit_, theme)
