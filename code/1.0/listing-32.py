"""Demonstrates text substitution using regular expressions with re.sub().

This script shows how to replace pattern matches in text using re.sub().
Readers learn regex substitution, pattern replacement, and text manipulation
with regular expressions.

"""
import logging
import re

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating regex substitution."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    text = "Hello, World! Welcome to the World of Python."
    pattern = r"World"
    replacement = "Python"

    new_text = re.sub(pattern, replacement, text)
    logger.info(f"Modified text: {new_text}")

    # Output:
    # Modified text: Hello, Python! Welcome to the World of Python.

if __name__ == "__main__":
    main()
