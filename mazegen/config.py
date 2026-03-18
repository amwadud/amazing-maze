from pathlib import Path
import os


# ── Custom exceptions ─────────────────────────────────────────────────────────


class DuplicateConfig(ValueError):
    """Raised when the same key appears more than once in the config file."""


class NoValidEntries(ValueError):
    """Raised when the config file has no parseable key=value pairs."""


class EmptyKey(ValueError):
    """Raised when a line has the form '=value' with no key."""


class InvalidSyntax(ValueError):
    """Raised when a line is not a comment, not blank, and has no '=' sign."""


# ── Config keys ───────────────────────────────────────────────────────────────

MANDATORY_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
OPTIONAL_KEYS = {"SEED"}
ALLOWED_KEYS = MANDATORY_KEYS | OPTIONAL_KEYS


# ── Parser ────────────────────────────────────────────────────────────────────


def parse_config(fp: str) -> dict[str, str]:
    """Parse a KEY=VALUE config file into a raw string dictionary.

    Lines starting with '#' and blank lines are ignored.
    Values are returned as raw strings — use validate_config() to type-cast them.

    Args:
        fp: Path to the configuration file.

    Returns:
        Dictionary mapping each key to its raw string value.

    Raises:
        TypeError:           If fp is not a string.
        FileNotFoundError:   If the file does not exist.
        ValueError:          If fp points to a directory.
        InvalidSyntax:       If a line has no '=' separator.
        EmptyKey:            If a line starts with '='.
        DuplicateConfig:     If the same key appears more than once.
        NoValidEntries:      If the file is empty or only has comments.
    """
    if not isinstance(fp, str):
        raise TypeError(f"fp must be a string, got {type(fp).__name__}")

    if not fp:
        raise ValueError("fp must not be an empty string")

    f_path = Path(fp)

    if not f_path.exists():
        raise FileNotFoundError(f"Config file not found: '{fp}'")

    if not f_path.is_file():
        raise ValueError(f"'{fp}' is not a file — it may be a directory")

    # Check read permission
    if not os.access(f_path, os.R_OK):
        raise PermissionError(f"File is not readable: '{fp}'")

    config: dict[str, str] = {}

    with f_path.open() as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise InvalidSyntax(f"Line {i}: missing '=' in '{line}'")

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                raise EmptyKey(f"Line {i}: empty key in '{line}'")

            if key in config:
                raise DuplicateConfig(f"Line {i}: duplicate key '{key}'")

            config[key] = value

    if not config:
        raise NoValidEntries("Config file is empty or contains only comments")

    return config


# ── Validator ─────────────────────────────────────────────────────────────────


def validate_config(config: dict[str, str]) -> dict:
    """Validate and type-cast raw config values from parse_config().

    Args:
        config: Raw string dictionary returned by parse_config().

    Returns:
        Dictionary with properly typed values:
            WIDTH       → int   (>= 3)
            HEIGHT      → int   (>= 3)
            ENTRY       → tuple[int, int]
            EXIT        → tuple[int, int]
            OUTPUT_FILE → str   (writable path)
            PERFECT     → bool
            SEED        → int   (default: 42 if not provided)

    Raises:
        ValueError: If any value is invalid or a mandatory key is missing.
    """
    validated: dict = {}

    # ── check all mandatory keys are present ──────────────────────────────────
    missing = MANDATORY_KEYS - config.keys()
    if missing:
        raise ValueError(
            f"Missing mandatory keys: {', '.join(sorted(missing))}"
        )

    # ── reject unknown keys ───────────────────────────────────────────────────
    unknown = config.keys() - ALLOWED_KEYS
    if unknown:
        raise ValueError(f"Unknown keys: {', '.join(sorted(unknown))}")

    # ── WIDTH ─────────────────────────────────────────────────────────────────
    try:
        validated["WIDTH"] = int(config["WIDTH"])
    except ValueError:
        raise ValueError("WIDTH must be an integer")
    if validated["WIDTH"] < 3:
        raise ValueError("WIDTH must be at least 3")

    # ── HEIGHT ────────────────────────────────────────────────────────────────
    try:
        validated["HEIGHT"] = int(config["HEIGHT"])
    except ValueError:
        raise ValueError("HEIGHT must be an integer")
    if validated["HEIGHT"] < 3:
        raise ValueError("HEIGHT must be at least 3")

    # ── ENTRY ─────────────────────────────────────────────────────────────────
    try:
        ex, ey = config["ENTRY"].split(",")
        entry = (int(ex.strip()), int(ey.strip()))
    except ValueError:
        raise ValueError("ENTRY must be in the format 'x,y' (e.g. '0,0')")
    if not (
        0 <= entry[0] < validated["WIDTH"]
        and 0 <= entry[1] < validated["HEIGHT"]
    ):
        raise ValueError(
            f"ENTRY {entry} is outside the maze bounds "
            f"({validated['WIDTH']}x{validated['HEIGHT']})"
        )
    validated["ENTRY"] = entry

    # ── EXIT ──────────────────────────────────────────────────────────────────
    try:
        xx, xy = config["EXIT"].split(",")
        exit_ = (int(xx.strip()), int(xy.strip()))
    except ValueError:
        raise ValueError("EXIT must be in the format 'x,y' (e.g. '19,14')")
    if not (
        0 <= exit_[0] < validated["WIDTH"]
        and 0 <= exit_[1] < validated["HEIGHT"]
    ):
        raise ValueError(
            f"EXIT {exit_} is outside the maze bounds "
            f"({validated['WIDTH']}x{validated['HEIGHT']})"
        )
    validated["EXIT"] = exit_

    if entry == exit_:
        raise ValueError("ENTRY and EXIT must not be the same cell")

    # ── OUTPUT_FILE ───────────────────────────────────────────────────────────
    filename = config["OUTPUT_FILE"]
    try:
        Path(filename).write_text("")
    except PermissionError:
        raise PermissionError(f"Cannot write to OUTPUT_FILE '{filename}'")
    except OSError as e:
        raise ValueError(f"Invalid OUTPUT_FILE path '{filename}': {e}")
    validated["OUTPUT_FILE"] = filename

    # ── PERFECT ───────────────────────────────────────────────────────────────
    perfect = config["PERFECT"].strip().lower()
    if perfect not in ("true", "false"):
        raise ValueError("PERFECT must be 'True' or 'False'")
    validated["PERFECT"] = perfect == "true"

    # ── SEED (optional, defaults to 42) ───────────────────────────────────────
    if "SEED" in config:
        try:
            validated["SEED"] = int(config["SEED"])
        except ValueError:
            raise ValueError("SEED must be an integer")
    else:
        validated["SEED"] = None

    return validated
