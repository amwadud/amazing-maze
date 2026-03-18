#!/usr/bin/env python3
import os
import random

from ascii_map.data_submitter import submit_data
from config import parse_config, validate_config
from display import THEMES, render_tui, animate_solution
from mazegen import create_generator, maze_solver


def main() -> None:
    config = validate_config(parse_config("config.txt"))
    maze = create_generator(
        config["WIDTH"],
        config["HEIGHT"],
        config["SEED"],
        config["PERFECT"],
    )
    maze.generate()
    theme = THEMES[37]
    show_path: bool = False
    path, path_directions = maze_solver(
        maze.grid, config["ENTRY"], config["EXIT"]
    )
    submit_data(config, maze, path_directions)
    try:
        while True:
            os.system("clear")
            render_tui(
                maze.grid,
                maze.width,
                maze.height,
                maze.locked,
                path if show_path else None,
                config["ENTRY"],
                config["EXIT"],
                theme,
            )
            print(f"{theme['WALL_COLOR']}\033[49m", end="")
            print("1) Regenerate")
            print(f"2) Change theme [current: {theme['name']}]")
            print("3) Toggle path")
            print("4) Animate solution")
            print("5) Quit")
            choice = input("Choose (based on number): ")
            print("\033[0m")  # reset color

            if choice == "1":
                maze.generate()
                path, path_directions = maze_solver(
                    maze.grid, config["ENTRY"], config["EXIT"]
                )
                submit_data(config, maze, path_directions)
            elif choice == "2":
                theme = random.choice([t for t in THEMES if t != theme])
            elif choice == "3":
                show_path = False if show_path else True
            elif choice == "4":
                animate_solution(
                    maze.grid,
                    maze.width,
                    maze.height,
                    maze.locked,
                    path,
                    config["ENTRY"],
                    config["EXIT"],
                    theme,
                )
                show_path = True
            elif choice == "5":
                print("See ya!")
                exit(0)
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as e:
        print(f"[ERROR]: {e}")


if __name__ == "__main__":
    main()
