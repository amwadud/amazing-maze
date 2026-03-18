from mazegen.constants import EAST, NORTH, WEST

RESET = "\033[0m"
EMPTY = "  "  # two spaces — matches "██" width


def _has(grid, x, y, d):
    """Returns True if cell (x, y) has a wall in direction d."""
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] & d


def _on_path(x, y, path, entry, exit_):
    """Check if cell is entry, exit, or on solution path."""
    return (x, y) in path or (x, y) == entry or (x, y) == exit_


def _gap(x1, y1, x2, y2, path, entry, exit_, theme):
    """Returns colored gap if both cells on path, otherwise empty."""
    # color the gap only if both neighboring cells are on the path
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


def render_tui(
    grid, w, h, locked=None, path=None, entry=None, exit_=None, theme=None
):
    """Renders the full maze in the terminal using block characters."""
    locked = locked or set()
    path = path or set()
    wall = theme["WALL_COLOR"] + "██" + RESET

    for y in range(h):
        row = []
        for x in range(w):
            row.append(wall)
            # open north = gap to cell above, closed = wall
            if _has(grid, x, y, NORTH):
                row.append(wall)
            else:
                row.append(_gap(x, y, x, y - 1, path, entry, exit_, theme))
        row.append(wall)
        print("".join(row))

        row = []
        for x in range(w):
            # open west = gap to cell on the left, closed = wall
            if _has(grid, x, y, WEST):
                row.append(wall)
            else:
                row.append(_gap(x, y, x - 1, y, path, entry, exit_, theme))
            row.append(_cell(x, y, locked, path, entry, exit_, theme))
        row.append(wall if _has(grid, w - 1, y, EAST) else EMPTY)
        print("".join(row))

    print(wall * (2 * w + 1))  # bottom border
