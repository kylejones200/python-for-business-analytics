"""Demonstrates basic variable assignment and arithmetic operations.

This script introduces fundamental Python concepts: variable assignment and
basic arithmetic. Readers learn how to assign values to variables and perform
simple calculations.

Chapter: Getting Started with Python for Analysis
Source: 1.0.tex
Extracted listing: 01
"""

import logging

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating basic variable operations."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # This is a cell with Python code
    a = 5
    b = a + 4
    logger.info(b)


if __name__ == "__main__":
    main()
