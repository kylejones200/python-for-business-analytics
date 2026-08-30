"""Demonstrates functions with return values.

This script shows how to define functions that return values and how to
capture those return values. Readers learn return statements and function
return value handling.

"""
import logging

logger = logging.getLogger(__name__)

def add_numbers(a, b):
    """Add two numbers and return the result.
    
    Args:
        a: First number.
        b: Second number.
    
    Returns:
        The sum of a and b.
    """
    return a + b

def main():
    """Main function demonstrating functions with return values."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    result = add_numbers(3, 5)
    logger.info(result)  # Output: 8

if __name__ == "__main__":
    main()
