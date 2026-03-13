# ── Wall bitmasks ─────────────────────────────────────────────────────────────
# Each cell stores a 4-bit integer. Each bit = one wall direction.
# 1 = wall is closed (solid), 0 = wall is open (passage).
#
#   bit 0 (value 1) = NORTH
#   bit 1 (value 2) = EAST
#   bit 2 (value 4) = SOUTH
#   bit 3 (value 8) = WEST
#
# Example: 0b0101 = 5 → NORTH and SOUTH walls closed, EAST and WEST open.
# A fully walled cell = 0b1111 = 0xF = 15.

NORTH = 0b0001  # 1
EAST  = 0b0010  # 2
SOUTH = 0b0100  # 4
WEST  = 0b1000  # 8


# ── Opposites ─────────────────────────────────────────────────────────────────
# When carving a passage between two cells, both must be updated.
# Example: moving EAST removes the EAST wall of cell A
#          AND the WEST wall of its neighbor cell B.

OPPOSITE: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST:  WEST,
    WEST:  EAST,
}


# ── Direction vectors ─────────────────────────────────────────────────────────
# Maps each direction to a (dx, dy) grid offset.
# Origin (0, 0) = top-left. Y increases downward.

DIRECTION: dict[int, tuple[int, int]] = {
    NORTH: (0, -1),
    EAST:  (1,  0),
    SOUTH: (0,  1),
    WEST:  (-1, 0),
}

# ── "42" pixel patterns ───────────────────────────────────────────────────────
# Two 5-row × 4-col grids of 1s and 0s.
# 1 = locked cell (fully walled, shown as ▓▓▓ in the TUI).
# 0 = normal maze cell.
# Both patterns have identical dimensions so they tile side by side.

PATTERN_4: list[list[int]] = [
    [1, 0, 0, 0],  # █ · · ·
    [1, 0, 0, 0],  # █ · · ·
    [1, 1, 1, 0],  # █ █ █ ·
    [0, 0, 1, 0],  # · · █ ·
    [0, 0, 1, 0],  # · · █ ·
]

PATTERN_2: list[list[int]] = [
    [1, 1, 1, 0],  # █ █ █ ·
    [0, 0, 1, 0],  # · · █ ·
    [1, 1, 1, 0],  # █ █ █ ·
    [1, 0, 0, 0],  # █ · · ·
    [1, 1, 1, 0],  # █ █ █ ·
]