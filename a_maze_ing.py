from mazegen import parse_config, validate_config
from mazegen import MazeGenerator
from display import renderer_tui


def main() -> None:
    try:
        config = validate_config(parse_config("config.txt"))
        maze = MazeGenerator(config["WIDTH"], config["HEIGHT"], config["SEED"])
        while True:
            maze.generate()
            renderer_tui.render_tui(
                maze.grid, maze.width, maze.height, maze.locked
            )
            print("1) Regenerate: ")
            print("1) Generate: ")
            input("Choose: ")
    except Exception as e:
         print(f"[Error]: {e}")


if __name__ == "__main__":
    main()
