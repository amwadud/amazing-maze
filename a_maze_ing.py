from mazegen.config_parser import config_parser


def main() -> None:
    try:
        config = config_parser("./config.txt")
        _ = config
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
