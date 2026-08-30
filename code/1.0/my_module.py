"""A tiny user-defined module for import demonstrations.

What you'll learn:
  - How to define constants and functions in a module
  - How other scripts can import and use your module

This file supports `code/1.0/listing-23.py`.
"""

import logging

logger = logging.getLogger(__name__)

PI = 3.14159


def greet(name: str) -> str:
    """Return a simple greeting.

    Args:
        name: Person name to greet.

    Returns:
        Greeting message.

    Raises:
        ValueError: If `name` is empty.
    """
    if not name:
        raise ValueError("name must be a non-empty string")
    return f"Hello, {name}!"


def main() -> None:
    """Demonstrate using this module as a script."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger.info("PI = %s", PI)
    logger.info("%s", greet("Alice"))


if __name__ == "__main__":
    main()
