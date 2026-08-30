"""Demonstrates a complete interactive game with loops and conditional logic.

This script implements a full number guessing game with user input validation,
loops, and conditional statements. Readers learn to structure game logic,
handle errors, and create interactive programs. The script works in both
interactive and non-interactive modes.

"""
import logging
import random
import sys

logger = logging.getLogger(__name__)

def main():
    """Main function implementing a complete number guessing game."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    random.seed(42)  # Set seed for reproducibility
    
    # Check if stdin is a TTY (interactive terminal)
    if not sys.stdin.isatty():
        logger.info("Non-interactive mode: skipping interactive game")
        logger.info("This game requires interactive input. Run interactively to play.")
        return

    # Generate a random number between 1 and 20
    secret_number = random.randint(1, 20)

    # Greet the player
    logger.info("Welcome to the Number Guessing Game!")
    name = input("What is your name? ")
    logger.info(f"\nHello, {name}! I'm thinking of a number between 1 and 20.")
    logger.info("You have 6 chances to guess it. Good luck!\n")

    # Game loop
    max_attempts = 6
    attempts = 0
    won = False

    while attempts < max_attempts:
        attempts += 1

        # Get the player's guess
        try:
            guess = int(input(f"Attempt {attempts}: Enter your guess: "))
        except ValueError:
            logger.warning("Please enter a valid number!")
            attempts -= 1
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

    # End game message
    if not won:
        logger.info(f"\nGame Over!")
        logger.info(f"Sorry, {name}. You've used all {max_attempts} attempts.")
        logger.info(f"The secret number was {secret_number}.")
        logger.info(f"Better luck next time!\n")

if __name__ == "__main__":
    main()
