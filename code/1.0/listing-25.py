"""Demonstrates date and time operations using the datetime module.

This script shows how to get the current date and time using datetime module
functions. Readers learn date and time handling, date.today(), and
datetime.now() methods.

"""
import logging
from datetime import date, datetime

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating date and time operations."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    current_date = date.today()
    current_time = datetime.now().time()

    logger.info(f"Current date: {current_date}")
    logger.info(f"Current time: {current_time}")

    # Output:
    # Current date: 2023-06-20
    # Current time: 14:30:45.123456

if __name__ == "__main__":
    main()
