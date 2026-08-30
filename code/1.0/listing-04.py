"""Demonstrates dictionary iteration using items() method.

This script shows how to iterate over dictionary key-value pairs using the
items() method. Readers learn dictionary iteration patterns and f-string
formatting for output.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating dictionary iteration."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    restaurant_rating = {"fast": 0, "Italian": 3, "Tex-Mex": 5}

    for k, v in restaurant_rating.items():
        logger.info(f"I give {k} food a rating of {v}")

    # Output: I give fast food a rating of 0
    # Output: I give Italian food a rating of 3
    # Output: I give Tex-Mex food a rating of 5

if __name__ == "__main__":
    main()
