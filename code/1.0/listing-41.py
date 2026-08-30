"""Demonstrates interactive game programming with random number generation.

This script introduces a number guessing game that uses random number generation
and user input. Readers learn to work with random numbers, handle user interaction,
and structure simple game logic. The script works in both interactive and
non-interactive modes.

Chapter: Getting Started with Python for Analysis
Source: 1.0.tex
Extracted listing: 41
"""
import logging
import random
import sys

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating a simple number guessing game setup."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    random.seed(42)  # Set seed for reproducibility
    
    # Check if stdin is a TTY (interactive terminal)
    if not sys.stdin.isatty():
        logger.info("Non-interactive mode: skipping interactive game")
        logger.info("This is a partial listing demonstrating game setup.")
        return
    
    # Generate a random number between 1 and 20
    secret_number = random.randint(1, 20)

    # Greet the player and get their name
    logger.info("Welcome to the Number Guessing Game!")
    name = input("What is your name? ")
    logger.info(f"\nHello, {name}! I'm thinking of a number between 1 and 20.")
    logger.info("You have 6 chances to guess it. Good luck!\n")

if __name__ == "__main__":
    main()