"""Demonstrates joining DataFrames using the join() method.

This script shows how to combine DataFrames using join() with different join
types. Readers learn DataFrame joining, join types (outer, inner, left, right),
and index-based joins.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 10
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating DataFrame joins."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    df1 = pd.DataFrame({"A": ["A0", "A1", "A2"], "B": ["B0", "B1", "B2"]})
    df2 = pd.DataFrame(
        {"C": ["C0", "C1", "C2"], "D": ["D0", "D1", "D2"]}, index=[0, 2, 3]
    )
    result = df1.join(df2, how="outer")
    logger.info(result)

if __name__ == "__main__":
    main()