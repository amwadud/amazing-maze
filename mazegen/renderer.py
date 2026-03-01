def render(grid: List[List[int]], width: int, height: int, locked: set = set()) -> None:
    # Box drawing characters
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

    def has_wall(x, y, direction):
        return grid[y][x] & direction

    # Top border
    line = TL
    for x in range(width):
        line += H * 2
        if x != width - 1:
            line += TJ
    line += TR
    print(line)

    # Rows
    for y in range(height):
        # Cell row
        row = V
        for x in range(width):
            if (x, y) in locked:
                row += "42"
            else:
                row += "  "

            # East wall
            if grid[y][x] & EAST:
                row += V
            else:
                row += " "
        print(row)

        # Horizontal walls between rows
        if y != height - 1:
            line = LJ
            for x in range(width):
                if grid[y][x] & SOUTH:
                    line += H * 2
                else:
                    line += "  "

                if x != width - 1:
                    line += CROSS
            line += RJ
            print(line)

    # Bottom border
    line = BL
    for x in range(width):
        line += H * 2
        if x != width - 1:
            line += BJ
    line += BR
    print(line)
