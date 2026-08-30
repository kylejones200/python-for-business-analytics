"""Demonstrates selective imports from the math module.

This script shows how to import specific functions and constants from a module
using the from...import syntax. Readers learn selective imports and the math
module's mathematical functions and constants.

"""
import logging
from math import sqrt, pi

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating selective imports."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    logger.info(sqrt(16))  # Output: 4.0
    logger.info(pi)  # Output: 3.141592653589793

if __name__ == "__main__":
    main()
