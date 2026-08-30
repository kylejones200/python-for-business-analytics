"""Demonstrates multiple exception handling with multiple except clauses.

This script shows how to handle different types of exceptions with multiple
except blocks. Readers learn multiple exception handling, FileNotFoundError,
IOError, and file operation error handling.

"""
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating multiple exception handling."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    try:
        file = open("nonexistent_file.txt", "r")
        content = file.read()
        file.close()
    except FileNotFoundError:
        logger.warning("Error: File not found!")
    except IOError:
        logger.warning("Error: Unable to read the file!")

    # Output:
    # Error: File not found!

if __name__ == "__main__":
    main()
