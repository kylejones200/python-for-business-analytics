"""Demonstrates regular expression pattern matching with re.findall().

This script shows how to find all matches of a pattern in text using regular
expressions. Readers learn regex patterns, re.findall(), and pattern matching
in Python.

"""
import logging
import re

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating regex pattern matching."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    text = "The price of the item is $19.99"
    pattern = r"\d+"

    matches = re.findall(pattern, text)
    logger.info(f"Matches: {matches}")

    # Output:
    # Matches: ['19', '99']

if __name__ == "__main__":
    main()
