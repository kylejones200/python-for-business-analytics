"""Demonstrates function definition and function calls.

This script shows function definition and calling patterns. Readers learn
to define functions and invoke them with arguments.

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
    # output: Hello, Alice!

if __name__ == "__main__":
    main()
