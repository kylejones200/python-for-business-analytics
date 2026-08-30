"""Handle user input in both interactive and non-interactive modes.
Demonstrates user input handling with interactive and non-interactive modes.

This script shows how to handle user input in Python, demonstrating the use of
input() for interactive prompts and providing fallback defaults for non-
interactive execution. Readers learn to write scripts that work both
interactively and in automated environments.

"""

import logging
import sys

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating user input handling."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Check if stdin is a TTY (interactive terminal)
    if sys.stdin.isatty():
        name = input("Enter your name: ")
    else:
        name = "Alice"  # Default for non-interactive execution
        logger.info(f"Non-interactive mode: using default name '{name}'")

    logger.info(f"Hello, {name}!")


if __name__ == "__main__":
    main()
