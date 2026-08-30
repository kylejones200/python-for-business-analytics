"""Demonstrates dictionary key access and value retrieval.

This script shows how to access dictionary values using keys. Readers learn
dictionary indexing syntax and how to retrieve values from dictionaries.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating dictionary key access."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Create example dictionary
    currency_map = {"Canada": "CAD", "US": "USD", "United Kingdom": "GBP"}
    
    result = currency_map["Canada"]  # Output: 'CAD'
    logger.info(result)

if __name__ == "__main__":
    main()
