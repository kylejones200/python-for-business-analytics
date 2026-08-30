"""Demonstrates game loop logic with input validation and conditional branching.

This script shows the core game loop for a number guessing game, demonstrating
while loops, exception handling for input validation, and conditional logic.
Readers learn to structure interactive game loops and handle user input errors.

Chapter: Getting Started with Python for Analysis
Source: 1.0.tex
Extracted listing: 42
"""
import logging
import random
import sys

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating game loop with input validation."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Check if stdin is a TTY (interactive terminal)
    if not sys.stdin.isatty():
        logger.info("Non-interactive mode: skipping interactive game loop")
        logger.info("This listing requires interactive input. Run interactively to play.")
        return
    
    # Initialize game variables
    import random
    random.seed(42)
    secret_number = random.randint(1, 20)
    name = "Player"  # Default name, can be set interactively
    max_attempts = 6
    attempts = 0
    won = False

    while attempts < max_attempts:
        attempts += 1

        # Get the player's guess and convert it to an integer
        try:
            guess = int(input(f"Attempt {attempts}: Enter your guess: "))
        except ValueError:
            logger.warning("Please enter a valid number!")
            attempts -= 1  # Don't count invalid input as an attempt
            continue

        # Check the guess
        if guess < secret_number:
            logger.info("Too low! Try a higher number.\n")
        elif guess > secret_number:
            logger.info("Too high! Try a lower number.\n")
        else:
            # They got it!
            won = True
            logger.info(f"\nCongratulations, {name}!")
            logger.info(f"You guessed the number {secret_number} in {attempts} tries!")
            break

if __name__ == "__main__":
    main()