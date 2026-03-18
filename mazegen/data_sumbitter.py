from typing import Any


def submit_data(
    config: dict[str, Any], maze: "MazeGenerator", path_directions: str
):
    try:
        with open(config["OUTPUT_FILE"], "w") as f:
            sections = []
            maze_lines = []
            for row in maze.grid:
                maze_lines.append(" ".join(hex(n) for n in row))
            sections.append("\n".join(maze_lines))
            entry = config["ENTRY"]

            sections.append(f"{entry[0]},{entry[1]}")
            exit_ = config["EXIT"]
            sections.append(f"{exit_[0]},{exit_[1]}")
            sections.append(path_directions)
            f.write("\n\n".join(sections))

    except Exception as e:
        print(f"[HMM]: {e}")
