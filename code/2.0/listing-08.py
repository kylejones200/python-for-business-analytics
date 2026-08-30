"""Demonstrates different DataFrame selection methods: loc, iloc, and query.

This script shows various ways to select data from DataFrames including
column selection, label-based selection (loc), position-based selection (iloc),
and query expressions. Readers learn different selection methods and when
to use each.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 08
"""
import logging

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating DataFrame selection methods."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Create example DataFrame
    import pandas as pd
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'London', 'Tokyo']
    })
    
    logger.info(df["Name"])  # Select column
    logger.info(df.loc[0])  # Select row by label
    logger.info(df.iloc[0])  # Select row by position
    logger.info(df.query("Age > 30"))  # Query DataFrame

if __name__ == "__main__":
    main()