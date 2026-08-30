"""Demonstrates lambda functions for simple anonymous functions.

This script introduces lambda functions as a concise way to define simple
functions. Readers learn lambda syntax and when to use lambda functions
versus regular function definitions.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating lambda functions."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    square = lambda x: x**2
    logger.info(square(5))  # Output: 25

if __name__ == "__main__":
    main()
