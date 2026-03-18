#!/usr/bin/env python3

from mazegen import parse_config, validate_config, maze_solver
from mazegen import MazeGenerator
from display import renderer_tui
import os


def main() -> None:
    # try:
    config = validate_config(parse_config("config.txt"))
    maze = MazeGenerator(config["WIDTH"], config["HEIGHT"], config["SEED"])
    path = None
    maze.generate()
    while True:
        os.system("clear")
        renderer_tui.render_tui(
            maze.grid,
            maze.width,
            maze.height,
            maze.locked,
            path,
            config["ENTRY"],
            config["EXIT"],
            # colors -> change maze colors
        )
        print("1) Regenerate: ")
        print("1) change colors: ")
        print("2) Toggle path")
        print("4) Quit")
        choice = input("Choose (based on number): ")
        if choice == 1:
            maze.generate()
            path, _ = maze_solver(  # the _ -> not gonna save path
                maze.grid, config["ENTRY"], config["EXIT"]
            )
        if choice == 2:
            pass
        if choice == 3:
            if path is not None:
                path, _ = maze_solver(
                    maze.grid, config["ENTRY"], config["EXIT"]
                )
            else:
                path = None
        elif choice == 4:
            print("See ya!")
            exit(0)
    # except Exception as e:
    #     print(f"[Error]: {e}")


if __name__ == "__main__":
    main()
