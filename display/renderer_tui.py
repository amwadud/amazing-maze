from mazegen.constants import NORTH, EAST, WEST

RESET = "\033[0m"
EMPTY = "  "


def _has(grid, x, y, d):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] & d


def _is_path_like(x, y, path, entry, exit_):
    """True for any cell that should visually
    connect through open corridors."""
    return (x, y) in path or (x, y) == entry or (x, y) == exit_


def _corridor(x1, y1, x2, y2, path, entry, exit_, theme):
    """Return a path-colored gap if both sides of
    an open corridor are on the path."""
    if _is_path_like(x1, y1, path, entry, exit_) and _is_path_like(x2, y2,
                                                                   path,
                                                                   entry,
                                                                   exit_):
        return theme["PATH_COLOR"] + EMPTY + RESET
    return EMPTY


def _cell(x, y, locked, path, entry, exit_, theme):
    if (x, y) == entry:
        color = theme["ENTRY_COLOR"]
    elif (x, y) == exit_:
        color = theme["EXIT_COLOR"]
    elif (x, y) in locked:
        color = theme["LOCKED_COLOR"]
    elif (x, y) in path:
        color = theme["PATH_COLOR"]
    else:
        color = theme["CELL_COLOR"]
    return color + EMPTY + RESET


def _render_top_wall_row(grid, w, y, path, entry, exit_, theme):
    wall = theme["WALL_COLOR"] + "██" + RESET
    segments = []
    for x in range(w):
        segments.append(wall)
        has_north_wall = _has(grid, x, y, NORTH)
        if has_north_wall:
            segments.append(wall)
        else:
            segments.append(_corridor(x, y, x, y - 1, path,
                                      entry, exit_, theme))
    segments.append(wall)
    print("".join(segments))


def _render_cell_row(grid, w, y, locked, path, entry, exit_, theme):
    wall = theme["WALL_COLOR"] + "██" + RESET
    segments = []
    for x in range(w):
        has_west_wall = _has(grid, x, y, WEST)
        if has_west_wall:
            segments.append(wall)
        else:
            segments.append(_corridor(x, y, x - 1, y, path,
                                      entry, exit_, theme))
        segments.append(_cell(x, y, locked, path, entry, exit_, theme))
    has_east_wall = _has(grid, w - 1, y, EAST)
    segments.append(wall if has_east_wall else EMPTY)
    print("".join(segments))


def render_tui(grid, w, h, locked=None, path=None,
               entry=None, exit_=None,  theme: dict[str, str] | None = None):
    locked = locked or set()
    path = path or set()

    for y in range(h):
        _render_top_wall_row(grid, w, y, path, entry, exit_, theme)
        _render_cell_row(grid, w, y, locked, path, entry, exit_, theme)

    wall = theme["WALL_COLOR"] + "██" + RESET
    print(wall * (2 * w + 1))
