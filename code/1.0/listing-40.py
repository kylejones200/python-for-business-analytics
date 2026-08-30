"""Demonstrates .format() method for string formatting.

This script shows how to use the .format() method for string formatting with
positional arguments and format specifiers. Readers learn .format() syntax,
format specifiers, and string formatting alternatives.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating .format() method."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    product = "Apple"
    price = 0.99
    quantity = 5
    message = "I bought {} {}s for a total cost of ${:.2f}.".format(
        quantity, product, price * quantity
    )
    logger.info(message)

if __name__ == "__main__":
    main()
