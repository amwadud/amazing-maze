from mazegen.constants import NORTH, EAST, WEST

RESET = "\033[0m"
WALL_COLOR = "\033[38;2;160;160;160m\033[48;2;30;30;30m"
CELL_COLOR = "\033[48;2;20;20;20m"
LOCKED_COLOR = "\033[38;2;255;255;255m\033[48;2;220;50;47m"
PATH_COLOR = "\033[38;2;0;0;0m\033[48;2;38;139;210m"
ENTRY_COLOR = "\033[38;2;0;0;0m\033[48;2;133;153;0m"
EXIT_COLOR = "\033[38;2;0;0;0m\033[48;2;255;140;0m"

WALL = WALL_COLOR + "██" + RESET
EMPTY = "  "


def _has(grid, x, y, d):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] & d


def _is_path_like(x, y, path, entry, exit_):
    """True for any cell that should visually connect through open corridors."""
    return (x, y) in path or (x, y) == entry or (x, y) == exit_


def _corridor(x1, y1, x2, y2, path, entry, exit_):
    """Return a path-colored gap if both sides of an open corridor are on the path."""
    if _is_path_like(x1, y1, path, entry, exit_) and _is_path_like(x2, y2, path, entry, exit_):
        return PATH_COLOR + EMPTY + RESET
    return EMPTY


def _cell(x, y, locked, path, entry, exit_):
    if (x, y) == entry:
        color = ENTRY_COLOR
    elif (x, y) == exit_:
        color = EXIT_COLOR
    elif (x, y) in locked:
        color = LOCKED_COLOR
    elif (x, y) in path:
        color = PATH_COLOR
    else:
        color = CELL_COLOR
    return color + EMPTY + RESET


def _render_top_wall_row(grid, w, y, path, entry, exit_):
    segments = []
    for x in range(w):
        segments.append(WALL)
        has_north_wall = _has(grid, x, y, NORTH)
        if has_north_wall:
            segments.append(WALL)
        else:
            segments.append(_corridor(x, y, x, y - 1, path, entry, exit_))
    segments.append(WALL)
    print("".join(segments))


def _render_cell_row(grid, w, y, locked, path, entry, exit_):
    segments = []
    for x in range(w):
        has_west_wall = _has(grid, x, y, WEST)
        if has_west_wall:
            segments.append(WALL)
        else:
            segments.append(_corridor(x, y, x - 1, y, path, entry, exit_))
        segments.append(_cell(x, y, locked, path, entry, exit_))
    has_east_wall = _has(grid, w - 1, y, EAST)
    segments.append(WALL if has_east_wall else EMPTY)
    print("".join(segments))


def render_tui(grid, w, h, locked=None, path=None, entry=None, exit_=None):
    locked = locked or set()
    path = path or set()

    for y in range(h):
        _render_top_wall_row(grid, w, y, path, entry, exit_)
        _render_cell_row(grid, w, y, locked, path, entry, exit_)

    bottom_wall = WALL * (2 * w + 1)
    print(bottom_wall)
