from pathlib import Path


class DuplicateConfig(ValueError):
    pass


class NoValidEntries(ValueError):
    pass


class EmptyKey(ValueError):
    pass


class InvalidSyntax(ValueError):
    pass


def parse_config(filepath: str) -> dict[str, str]:
    """Parse a KEY=VALUE config file.

    Args:
        filepath: Path to the configuration file.

    Returns:
        Dictionary of key-value pairs.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If a line has invalid syntax.
    """
    config = {}

    # TODO: validate that filepath is not an empty string before even trying
    # TODO: validate required keys after parsing (WIDTH, HEIGHT, ENTRY, EXIT, etc.)
    # TODO: validate value types (WIDTH should be int, PERFECT should be bool, etc.)
    # TODO: validate that ENTRY and EXIT are within maze bounds
    # TODO: decide max file size limit? a huge config file would be unusual

    try:
        f_path = Path(filepath)
    except TypeError:
        # Path() raises TypeError if filepath is None or not a string
        raise TypeError(f"filepath must be a string, got {type(filepath).__name__}")

    if not f_path.exists():
        raise FileNotFoundError(f"Config file not found: '{filepath}'")

    if not f_path.is_file():
        # catches the case where filepath points to a directory
        raise ValueError(f"'{filepath}' is not a file")

    with f_path.open() as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            try:
                key, value = line.split('=', 1)
            except ValueError:
                raise InvalidSyntax(f"Invalid syntax on line {i}: '{line}'")

            key = key.strip()
            value = value.strip()

            if key in config:
                raise DuplicateConfig(f"Duplicate key '{key}' on line {i}")

            if not key:
                # catches a line like "=somevalue"
                raise EmptyKey(f"Empty key on line {i}: '{line}'")

            config[key] = value

    if not config:
        raise NoValidEntries("Config file is empty or has no valid entries")

    return config


def validate_config(config: dict[str, str]):
    mandatory_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    ]

    addational_keys = [
        "SEED",
        "ALGO",
        "MODE"
    ]
    clean_config = {}

    for key, value in config:
        if key not in mandatory_keys or not value:
            if key not in addational_keys or not value:
                raise ValueError()
        # Width
        if key == "WIDTH":
            try:
                config[key] = int(value)
                if config[key] < 0:
                    raise ValueError("width cannot be negative.")
                elif config[key] < 3:
                    raise ValueError("width must be greater than"
                                     " or equal to 3")
                else:
                    clean_config[key] = int(value)
            except ValueError:
                raise ValueError("the value width is error")
        if key == "HEIGHT":
            try:
                config[key] = int(value)
                if config[key] < 0:
                    raise ValueError("height cannot be negative.")
                elif config[key] < 3:
                    raise ValueError("height must be greater than"
                                     " or equal to 3")
                else:
                    clean_config[key] = int(value)
            except ValueError:
                raise ValueError("the value height is error")
