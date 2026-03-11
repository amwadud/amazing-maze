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
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
]

PATTERN_2 = [
    [1, 1, 1, 0],
    [0, 0, 1, 0],
    [1, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 1, 1, 0],
]
