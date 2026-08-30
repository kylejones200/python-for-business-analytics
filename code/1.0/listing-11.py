"""Demonstrates array manipulation methods: append and remove.

This script shows how to modify arrays using append() and remove() methods.
Readers learn array mutation operations and the importance of type precision
for floating-point comparisons.

"""

import array
import logging

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating array manipulation."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Use double precision for reliable equality comparisons when removing
    # floats.
    grades = array.array("d", [85.5, 90.2, 92.9])
    grades.append(88.9)
    grades.remove(90.2)
    logger.info(grades)
    # Output: array('d', [85.5, 92.9, 88.9])


if __name__ == "__main__":
    main()
