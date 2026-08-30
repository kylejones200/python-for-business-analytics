"""Demonstrates lambda functions with multiple parameters.

This script shows lambda functions that take multiple arguments. Readers
learn to create multi-parameter lambda functions for concise operations.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating multi-parameter lambda functions."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    multiply = lambda x, y: x * y
    logger.info(multiply(3, 4))  # Output: 12

if __name__ == "__main__":
    main()
