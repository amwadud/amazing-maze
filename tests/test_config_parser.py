import tempfile
import os
from mazegen.parser_config import parse_config


def create_temp_config(content: str) -> str:
    """Create a temporary config file with given content.

    Args:
        content: The text to write into the temp file.

    Returns:
        The path to the temporary file as a string.
    """
    tmp = tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', delete=False
    )
    tmp.write(content)
    tmp.close()
    return tmp.name


def run_test(name: str, fn) -> None:
    """Run a single test function and print result.

    Args:
        name: The test name to display.
        fn: The test function to call.
    """
    try:
        fn()
        print(f"  PASS  {name}")
    except AssertionError as e:
        print(f"  FAIL  {name} → {e}")
    except Exception as e:
        print(f"  ERROR {name} → {type(e).__name__}: {e}")


# ── tests ────────────────────────────────────────────────────────────────────

def test_valid_config():
    path = create_temp_config(
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
    )
    try:
        result = parse_config(path)
        assert result == {"WIDTH": "20", "HEIGHT": "15", "ENTRY": "0,0"}
    finally:
        os.unlink(path)


def test_comments_and_blank_lines():
    path = create_temp_config(
        "# this is a comment\n"
        "\n"
        "WIDTH=20\n"
    )
    try:
        result = parse_config(path)
        assert result == {"WIDTH": "20"}
    finally:
        os.unlink(path)


def test_empty_key_raises():
    path = create_temp_config("=20\n")
    try:
        parse_config(path)
        raise AssertionError("Expected ValueError but nothing was raised")
    except ValueError as e:
        assert "Empty key on line 1" in str(e), f"Wrong message: {e}"
    finally:
        os.unlink(path)


def test_invalid_syntax_raises():
    path = create_temp_config("WIDTHBAD\n")
    try:
        parse_config(path)
        raise AssertionError("Expected ValueError but nothing was raised")
    except ValueError as e:
        assert "Invalid syntax on line 1" in str(e), f"Wrong message: {e}"
    finally:
        os.unlink(path)


def test_duplicate_key_raises():
    path = create_temp_config(
        "WIDTH=20\n"
        "WIDTH=30\n"
    )
    try:
        parse_config(path)
        raise AssertionError("Expected ValueError but nothing was raised")
    except ValueError as e:
        assert "Duplicate key 'WIDTH' on line 2" in str(e), \
            f"Wrong message: {e}"
    finally:
        os.unlink(path)


def test_file_not_found():
    try:
        parse_config("nonexistent_file.txt")
        raise AssertionError("Expected FileNotFoundError but nothing was raised")
    except FileNotFoundError:
        pass


def test_empty_file_raises():
    path = create_temp_config("")
    try:
        parse_config(path)
        raise AssertionError("Expected ValueError but nothing was raised")
    except ValueError as e:
        assert "empty" in str(e).lower(), f"Wrong message: {e}"
    finally:
        os.unlink(path)


def test_strips_whitespace():
    path = create_temp_config("  WIDTH  =  20  \n")
    try:
        result = parse_config(path)
        assert result == {"WIDTH": "20"}
    finally:
        os.unlink(path)


# ── runner ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        ("valid config", test_valid_config),
        ("comments and blank lines", test_comments_and_blank_lines),
        ("empty key raises", test_empty_key_raises),
        ("invalid syntax raises", test_invalid_syntax_raises),
        ("duplicate key raises", test_duplicate_key_raises),
        ("file not found", test_file_not_found),
        ("empty file raises", test_empty_file_raises),
        ("strips whitespace", test_strips_whitespace),
    ]

    print(f"\nRunning {len(tests)} tests...\n")
    for name, fn in tests:
        run_test(name, fn)
    print()
