"""Demonstrates importing and using custom modules.

This script shows how to import a custom module and access its functions and
constants. Readers learn module import syntax and how to use imported
functions and variables.

"""

import logging

logger = logging.getLogger(__name__)

try:
    import my_module
except ImportError:
    logger.error(
        "my_module not found. This listing requires my_module.py in the same "
        "directory."
    )
    raise SystemExit(1)


def main():
    """Main function demonstrating module imports."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    logger.info(my_module.greet("Alice"))  # Output: Hello, Alice!
    logger.info(my_module.PI)  # Output: 3.14159


if __name__ == "__main__":
    main()
