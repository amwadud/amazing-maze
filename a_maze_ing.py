#!/usr/bin/env python3

from mazegen import parse_config, validate_config, maze_solver
from mazegen import MazeGenerator
from display import renderer_tui
import os


def main() -> None:
    # try:
    config = validate_config(parse_config("config.txt"))
    maze = MazeGenerator(config["WIDTH"], config["HEIGHT"], config["SEED"])
    while True:
        os.system("clear")
        maze.generate()
        path, dir_path = maze_solver(
            maze.grid, config["ENTRY"], config["EXIT"]
        )
        renderer_tui.render_tui(
            maze.grid,
            maze.width,
            maze.height,
            maze.locked,
            None,
            config["ENTRY"],
            config["EXIT"],
        )
        print("1) Regenerate: ")
        print("1) change colors: ")
        print("3) Quit")
        choice = input("Choose (based on number): ")
        if choice == 2:
            pass
        elif choice == 3:
            pass
    # except Exception as e:
    #     print(f"[Error]: {e}")


if __name__ == "__main__":
    main()
