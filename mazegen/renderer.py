#!/usr/bin/env python3
"""Maze renderer module.

Renders the maze grid to the terminal using box-drawing characters.
"""

import globals
from globals import EAST, SOUTH, RESET, CELL, LOCKED, PATH
from globals import ENTRY_COLOR, EXIT_COLOR


def renderer(
    grid: list[list[int]],
    width: int,
    height: int,
    locked: set = set(),
    path_cells: list[tuple[int, int]] | None = None,
    entry: tuple[int, int] | None = None,
    exit_: tuple[int, int] | None = None,
) -> None:
    """Render the maze in the terminal.

    Args:
        grid: The maze grid as grid[y][x].
        width: Number of columns.
        height: Number of rows.
        locked: Set of (x, y) cells that are part of the 42 pattern.
        path_cells: Ordered list of (x, y) cells on the solution path.
        entry: Entry cell as (x, y) shown in green.
        exit_: Exit cell as (x, y) shown in red.
    """
    H = "━"
    V = "┃"
    TL = "┏"
    TR = "┓"
    BL = "┗"
    BR = "┛"
    TJ = "┳"
    BJ = "┻"
    LJ = "┣"
    RJ = "┫"
    CROSS = "╋"

    path_set: set[tuple[int, int]] = (
        set(path_cells) if path_cells is not None else set()
    )

    def cell_color(x: int, y: int) -> str:
        """Return the ANSI color for a cell.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            ANSI color string.
        """
        if (x, y) == entry:
            return ENTRY_COLOR
        if (x, y) == exit_:
            return EXIT_COLOR
        if (x, y) in locked:
            return LOCKED
        if (x, y) in path_set:
            return PATH
        return CELL

    def cell_text(x: int, y: int) -> str:
        """Return the 2-character text drawn inside a cell.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            2-character string for cell content.
        """
        if (x, y) == entry:
            return "EN"
        if (x, y) == exit_:
            return "EX"
        if (x, y) in locked:
            return "42"
        return "  "

    # --- Top border ---
    line = globals.WALL + TL
    for x in range(width):
        line += H * 2
        if x != width - 1:
            line += TJ
    line += TR + RESET
    print(line)

    # --- Rows ---
    for y in range(height):

        # Cell row
        row = globals.WALL + V + RESET
        for x in range(width):
            color = cell_color(x, y)
            text = cell_text(x, y)
            row += color + text + RESET

            # East wall
            if grid[y][x] & EAST:
                row += globals.WALL + V + RESET
            else:
                if x + 1 < width:
                    row += cell_color(x + 1, y) + " " + RESET
                else:
                    row += CELL + " " + RESET

        print(row)

        # Horizontal walls between rows
        if y != height - 1:
            line = globals.WALL + LJ
            for x in range(width):
                if grid[y][x] & SOUTH:
                    line += H * 2
                else:
                    line += RESET + cell_color(x, y) + "  " + RESET + globals.WALL
                if x != width - 1:
                    line += CROSS
            line += RJ + RESET
            print(line)

    # --- Bottom border ---
    line = globals.WALL + BL
    for x in range(width):
        line += H * 2
        if x != width - 1:
            line += BJ
    line += BR + RESET
    print(line)
