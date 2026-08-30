"""Demonstrates generating descriptive statistics with DataFrame.describe().

This script shows how to use the describe() method to get summary statistics
for numeric columns in a DataFrame. Readers learn descriptive statistics,
DataFrame methods, and data exploration techniques.

"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating descriptive statistics."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Create example DataFrame
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [10, 11, 12, 13, 14]})
    logger.info("Descriptive statistics:\n%s", df.describe())

if __name__ == "__main__":
    main()
