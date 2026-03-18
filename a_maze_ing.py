#!/usr/bin/env python3
from mazegen import parse_config, validate_config, maze_solver
from mazegen import MazeGenerator
from display import renderer_tui
import os


def main() -> None:
    # try:
    config = validate_config(parse_config("config.txt"))
    maze = MazeGenerator(config["WIDTH"], config["HEIGHT"], config["SEED"])
    maze.generate()
    path, _ = maze_solver(
        maze.grid, config["ENTRY"], config["EXIT"]
    )

    path = None
    show_path: bool = False
    while True:
        os.system("clear")
        renderer_tui.render_tui(
            maze.grid,
            maze.width,
            maze.height,
            maze.locked,
            path if show_path else None,
            config["ENTRY"],
            config["EXIT"],
            # colors -> change maze colors
        )

        print("1) Regenerate")
        print("2) Change colors")
        print("3) Toggle path")
        print("4) Quit")
        choice = input("Choose (based on number): ")

        if choice == "1":
            maze.generate()
            path, _ = maze_solver(
                maze.grid, config["ENTRY"], config["EXIT"]
            )

        elif choice == "2":
            pass

        elif choice == "3":
            show_path = False if show_path else True

        elif choice == "4":
            print("See ya!")
            exit(0)
    # except Exception as e:
    #     print(f"[Error]: {e}")


if __name__ == "__main__":
    main()
