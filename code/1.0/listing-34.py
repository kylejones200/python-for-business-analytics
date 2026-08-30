"""Demonstrates listing installed packages using pip (documentation example).

This script serves as a documentation example showing pip list command syntax.
Readers learn how to view installed Python packages using pip.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating pip list documentation."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    logger.info("This listing demonstrates pip list syntax:")
    logger.info("# pip list")
    logger.info("Run this command in your terminal to list installed packages.")

if __name__ == "__main__":
    main()
