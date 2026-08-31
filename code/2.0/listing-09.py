"""Demonstrates handling missing values with dropna() and fillna().

This script shows how to detect, remove, and fill missing values in
DataFrames. Readers learn missing data detection, data cleaning techniques,
and imputation strategies.

Chapter: Understanding Data Before Modeling Source: 2.0.tex Extracted listing:
09
"""

import logging

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating missing value handling."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Create example DataFrame with missing values
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame(
        {
            'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
            'Age': [25, np.nan, 35, 28],
            'City': ['New York', 'London', np.nan, 'Tokyo'],
        }
    )

    # Check for missing values
    logger.info("Missing values:\n%s", df.isnull().sum())

    # Drop rows with any missing values
    df_cleaned = df.dropna()
    logger.info(f"Dropped rows: {len(df) - len(df_cleaned)} rows removed")

    # Fill missing values
    df_filled = df.fillna(0)
    logger.info("Missing values filled with 0")


if __name__ == "__main__":
    main()
