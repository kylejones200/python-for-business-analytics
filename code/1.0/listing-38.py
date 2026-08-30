"""Demonstrates type conversion and basic arithmetic with user input.

This script shows how to convert string input to integers and perform calculations.
Readers learn input validation, type conversion, and basic arithmetic operations
in Python.

"""
import logging
import sys

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating type conversion and arithmetic."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Check if stdin is a TTY (interactive terminal)
    if sys.stdin.isatty():
        try:
            age = int(input("Enter your age: "))
        except ValueError:
            logger.error("Invalid input. Please enter a valid integer.")
            age = 29  # Default fallback
            logger.info(f"Using default age: {age}")
    else:
        age = 29  # Default for non-interactive execution
        logger.info(f"Non-interactive mode: using default age {age}")
    
    next_year = age + 1
    logger.info(f"Next year, you will be {next_year}!")
    # Output: Next year, you will be 30!

if __name__ == "__main__":
    main()
