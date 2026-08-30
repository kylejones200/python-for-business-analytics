"""Demonstrates dictionary creation and representation.

This script shows how to create dictionaries in Python using key-value pairs.
Readers learn dictionary syntax and how dictionaries are represented when
displayed.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating dictionary creation."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    currency_map = {"Canada": "CAD", "US": "USD", "United Kingdom": "GBP"}
    logger.info(currency_map)
    # Output: {'Canada': 'CAD', 'US': 'USD', 'United Kingdom': 'GBP'}

if __name__ == "__main__":
    main()
