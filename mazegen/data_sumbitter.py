from typing import Any


def _get_maze_as_hex(maze: list[list[int]]) -> str:
    for row in maze:
        line = [str(hex(n)) for n in row]



def submit_data(config: dict[str, Any], path_directions: str):
    # submit the maze as hex
    try:
        with open(config["OUTPUT_FILE"], "w") as f:
            pass
    except Exception as e:
        print(f"[HMM]: {e}")
