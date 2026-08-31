"""Demonstrates conditional logic for game end scenarios.

This script shows how to handle game ending conditions with conditional
statements. Readers learn conditional logic, game state management, and
user feedback patterns.

Chapter: Getting Started with Python for Analysis
Source: 1.0.tex
Extracted listing: 43
"""

import logging

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating game end condition handling."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Simulate game end scenario
    import random

    random.seed(42)
    max_attempts = 6
    name = "Player"
    secret_number = random.randint(1, 20)
    won = False  # Simulate losing scenario

    # If they didn't win, tell them the answer
    if not won:
        logger.info(f"\nGame Over!")
        logger.info(
            f"Sorry, {name}. You've used all {max_attempts} attempts."
        )
        logger.info(f"The secret number was {secret_number}.")
        logger.info(f"Better luck next time!\n")


if __name__ == "__main__":
    main()
