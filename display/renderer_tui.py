from mazegen.constants import NORTH, EAST, WEST

CELL_WIDTH = 3  # width of cell content
WALL = "███"     # uniform wall thickness

def _has(grid, x, y, d):
    h = len(grid)
    w = len(grid[0]) if h else 0
    return 0 <= x < w and 0 <= y < h and bool(grid[y][x] & d)

def _cell_symbol(x, y, locked, path, entry, exit_):
    if (x, y) in locked:
        return "▓" * CELL_WIDTH
    if (x, y) in path:
        return " · "
    if (x, y) == entry:
        return " ▶ "
    if (x, y) == exit_:
        return " ■ "
    return " " * CELL_WIDTH

def render_tui(grid, width, height, locked=None, path=None, entry=None, exit_=None):
    locked = locked or set()
    path = path or set()

    for y in range(height):
        # Top wall line
        line_top = []
        for x in range(width):
            line_top.append(WALL)  # top-left corner of cell
            line_top.append(WALL if _has(grid, x, y, NORTH) else " " * CELL_WIDTH)
        line_top.append(WALL)  # rightmost corner
        print("".join(line_top))

        # Cell content + vertical walls
        line_cells = []
        for x in range(width):
            line_cells.append(WALL if _has(grid, x, y, WEST) else " " * len(WALL))
            line_cells.append(_cell_symbol(x, y, locked, path, entry, exit_))
        line_cells.append(WALL if _has(grid, width-1, y, EAST) else " " * len(WALL))
        print("".join(line_cells))

    # Bottom wall line (always solid)
    line_bottom = []
    for x in range(width):
        line_bottom.append(WALL)
        line_bottom.append(WALL)
    line_bottom.append(WALL)
    print("".join(line_bottom))