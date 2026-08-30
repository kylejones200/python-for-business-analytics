"""Demonstrates module-level function and constant definitions.

This script shows how to define functions and constants at the module level
for use in other modules. Readers learn module structure and how to create
reusable code modules.

"""
import logging

logger = logging.getLogger(__name__)

def greet(name):
    """Greet a person by name.
    
    Args:
        name: The name of the person to greet.
    
    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"

PI = 3.14159  # Module-level constant

def main():
    """Main function demonstrating module-level definitions."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    logger.info(greet("Alice"))
    logger.info(f"PI constant: {PI}")

if __name__ == "__main__":
    main()
