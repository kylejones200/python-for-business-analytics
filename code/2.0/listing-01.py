"""Demonstrates checking Python version information.

This script shows how to access Python version information using the sys module.
Readers learn to check Python version compatibility and system information.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 01
"""
import logging
import sys

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating version checking."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    logger.info(sys.version)


if __name__ == "__main__":
    main()
