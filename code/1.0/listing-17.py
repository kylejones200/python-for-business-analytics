"""Demonstrates built-in iter() and next() functions for manual iteration.

This script shows how to manually iterate over sequences using iter() and
next() functions. Readers learn explicit iterator creation and manual
iteration control.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating manual iteration."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    my_list = [1, 2, 3, 4, 5]
    my_iterator = iter(my_list)

    logger.info(next(my_iterator))  # Output: 1
    logger.info(next(my_iterator))  # Output: 2
    logger.info(next(my_iterator))  # Output: 3

if __name__ == "__main__":
    main()
