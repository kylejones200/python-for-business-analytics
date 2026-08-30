"""Demonstrates date parsing and timedelta arithmetic operations.

This script shows how to parse date strings using strptime() and perform
date arithmetic with timedelta. Readers learn date parsing, format strings,
and date arithmetic operations.

"""
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating date parsing and arithmetic."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Parse a date string
    date_string = "2023-06-20"
    parsed_date = datetime.strptime(date_string, "%Y-%m-%d")

    # Add 7 days to the parsed date
    future_date = parsed_date + timedelta(days=7)

    logger.info(f"Parsed date: {parsed_date}")
    logger.info(f"Future date: {future_date}")

    # Output:
    # Parsed date: 2023-06-20 00:00:00
    # Future date: 2023-06-27 00:00:00

if __name__ == "__main__":
    main()
