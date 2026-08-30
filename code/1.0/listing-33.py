"""Demonstrates package installation using pip (documentation example).

This script serves as a documentation example showing pip install command
syntax. Readers learn how to install Python packages using pip.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating pip installation documentation."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    logger.info("This listing demonstrates pip install syntax:")
    logger.info("# pip install package_name")
    logger.info("Run this command in your terminal to install packages.")

if __name__ == "__main__":
    main()
