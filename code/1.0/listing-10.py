"""Demonstrates the array module for efficient numeric arrays.

This script introduces the array module for creating typed arrays of numeric
values. Readers learn array creation, type codes, and array indexing.

"""
import array
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating array module usage."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    numbers = array.array("i", [1, 2, 3, 4, 5])
    logger.info(numbers[0])  # Output: 1
    logger.info(numbers[2])  # Output: 3

if __name__ == "__main__":
    main()
