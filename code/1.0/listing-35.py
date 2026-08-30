"""Demonstrates exception handling with try-except blocks.

This script shows how to catch and handle specific exceptions using
try-except. Readers learn exception handling, ZeroDivisionError, and
error management in Python.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating exception handling."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.warning("Error: Division by zero!")

    # Output:
    # Error: Division by zero!

if __name__ == "__main__":
    main()
