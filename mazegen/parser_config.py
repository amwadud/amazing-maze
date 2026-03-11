from pathlib import Path


class DuplicateConfig(ValueError):
    pass


class NoValidEntries(ValueError):
    pass


class EmptyKey(ValueError):
    pass


class InvalidSyntax(ValueError):
    pass


class Point:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        """Initialize a Point with x and y coordinates.

        Args:
            x: The horizontal coordinate.
            y: The vertical coordinate.
        """
        self.x = x
        self.y = y


def parse_config(fp: str) -> dict[str, str]:
    """Parse a KEY=VALUE config file.

    Args:
        fp: Path to the configuration file.

    Returns:
        Dictionary of key-value pairs.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If a line has invalid syntax.
    """
    config = {}

    # TODO: validate that fp is not an empty string before even trying
    # TODO: validate required keys after parsing (WIDTH, HEIGHT, ENTRY, EXIT, etc.)
    # TODO: validate value types (WIDTH should be int, PERFECT should be bool, etc.)
    # TODO: validate that ENTRY and EXIT are within maze bounds
    # TODO: decide max file size limit? a huge config file would be unusual

    try:
        f_path = Path(fp)
    except TypeError:
        # Path() raises TypeError if fp is None or not a string
        raise TypeError(f"fp must be a string, got {type(fp).__name__}")

    if not f_path.exists():
        raise FileNotFoundError(f"Config file not found: '{fp}'")

    if not f_path.is_file():
        # catches the case where fp points to a directory
        raise ValueError(f"'{fp}' is not a file")

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
    """Validate and convert raw config values into their proper types.

    Args:
        config: Raw string dictionary from parse_config.

    Returns:
        Clean dictionary with properly typed values.

    Raises:
        ValueError: If any value is invalid or a mandatory key is missing.
    """
    mandatory_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "OUTPUT_FILE", "PERFECT"}
    optional_keys = {"SEED"}
    allowed_keys = mandatory_keys | optional_keys
    validated = {}

    for key in mandatory_keys:
        if key not in config:
            raise ValueError(f"[ERROR]: Missing mandatory key '{key}'")

    for key, value in config.items():
        if key not in allowed_keys:
            raise ValueError(f"[ERROR]: Unknown key '{key}'")

        if not value:
            raise ValueError(f"[ERROR]: Value for '{key}' cannot be empty")
        # Width
        if key == "WIDTH":
            # FIXME: andle that we shouldn't print
            # FIXME: 42 pattern in case of be less than 3
            try:
                validated[key] = int(value)
            except ValueError:
                raise ValueError("[ERROR]: WIDTH must be an integer")
            if validated[key] < 3:
                raise ValueError("[ERROR]: WIDTH must be greater than 2")

        if key == "HEIGHT":
            try:
                validated[key] = int(value)
            except ValueError:
                raise ValueError("[ERROR]: HEIGHT must be an integer")
            if validated[key] < 3:
                raise ValueError("[ERROR]: HEIGHT must be greater than 2")

        if key == "ENTRY":
            # Parsing the 0,0 value
            entry = Point()
            entry.x, entry.y = value.split(',')
            entry.x = int(entry.x)
            entry.y = int(entry.y)

        if key == "EXIT":
            # Parsing the 0,0 value
            target = Point()
            target.x, target.y = value.split(',')
            target.x = int(target.x)
            target.y = int(target.y)

        if key == "OUTPUT_FILE":
            filename = value
            try:
                with open(filename, 'w') as f:
                    f.write("")
            except PermissionError:
                raise PermissionError("[ERROR]: Cannot write to file.")
            validated[key] = filename

        if key == "PERFECT":
            value = value.lower()
            if value != "false" and value != "true":
                raise ValueError("[ERROR]: PERFECT must be 'True' or 'False'")
            value = value == "true"
            validated[key] = value

        if key == "SEED":
            try:
                validated[key] = int(value)
            except ValueError:
                raise ValueError("[ERROR]: Seed should be a number.")

    # FIXME: check that
    if "SEED" not in validated:
        validated.setdefault("SEED", 42)

    return validated
