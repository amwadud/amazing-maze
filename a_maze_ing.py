#!/usr/bin/env python3
from mazegen import (
    parse_config,
    validate_config,
    maze_solver,
    MazeGenerator,
    COLOR_THEMES,
    submit_data
)
from display import renderer_tui
import os
import random


def main() -> None:
    config = validate_config(parse_config("config.txt"))
    maze = MazeGenerator(config["WIDTH"], config["HEIGHT"], config["SEED"])
    maze.generate()
    theme = COLOR_THEMES[0]
    show_path: bool = False
    path, path_directions = maze_solver(
        maze.grid, config["ENTRY"], config["EXIT"]
    )

    try:
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
                theme
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
                submit_data(config, path_directions)

            elif choice == "2":
                theme = random.choice([t for t in COLOR_THEMES if t != theme])

            elif choice == "3":
                show_path = False if show_path else True

            elif choice == "4":
                print("See ya!")
                exit(0)
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as e:
        print(f"[ERROR]: {e}")


if __name__ == "__main__":
    main()
