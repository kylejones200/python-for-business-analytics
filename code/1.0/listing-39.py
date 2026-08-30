"""Demonstrates f-string formatting for string interpolation.

This script shows how to use f-strings to embed variables in strings.
Readers learn f-string syntax, string interpolation, and modern Python
string formatting.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating f-string formatting."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    name = "Alice"
    age = 25
    message = f"My name is {name} and I am {age} years old."
    logger.info(message)  # Output: My name is Alice and I am 25 years old.

if __name__ == "__main__":
    main()
