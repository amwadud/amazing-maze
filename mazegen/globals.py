# Gruvbox colors (ANSI escape codes)
# [*ANSI = a standard for colors in the terminal*]
RESET = "\033[0m"
WALL = "\033[38;2;60;56;54m\033[48;2;28;28;28m"   # very dark grey walls
CELL = "\033[48;2;80;73;69m"                        # medium grey cells
LOCKED = "\033[38;2;255;255;255m\033[48;2;204;36;29m"  # white text, red bg
PATH = "\033[38;2;40;40;40m\033[48;2;184;187;38m"   # dark text, yellow bg
ENTRY_COLOR = "\033[38;2;255;255;255m\033[48;2;152;190;50m"  # green for entry
EXIT_COLOR = "\033[38;2;255;255;255m\033[48;2;251;73;52m"   # red for exit

# Wall bits
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

DIRECTION = {
    'N': (0, -1, NORTH),
    'E': (1, 0, EAST),
    'S': (0, 1, SOUTH),
    'W': (-1, 0, WEST),
}

PATTERN_4 = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1],
]

PATTERN_2 = [
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
]
