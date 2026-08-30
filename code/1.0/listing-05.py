"""Demonstrates function definition and function calls.

This script introduces function definition syntax and how to call functions
with arguments. Readers learn to create reusable code blocks using functions.

"""
import logging

logger = logging.getLogger(__name__)

def greet(name):
    """Greet a person by name.
    
    Args:
        name: The name of the person to greet.
    """
    logger.info(f"Hello, {name}!")

def main():
    """Main function demonstrating function calls."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    greet("Alice")
    # Output: Hello, Alice!

if __name__ == "__main__":
    main()
