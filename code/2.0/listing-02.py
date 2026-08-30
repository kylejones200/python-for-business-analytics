"""Demonstrates creating pandas Series from different data sources.

This script shows how to create pandas Series objects from lists, NumPy arrays,
and dictionaries. Readers learn Series creation, indexing, and pandas data
structures.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 02
"""
import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating Series creation."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Creating a Series from a list
    s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])
    logger.info("Pandas Series:\n%s", s)

    # Creating a Series from a NumPy array
    s_np = pd.Series(np.arange(5))
    logger.info("\nSeries from NumPy array:\n%s", s_np)

    # Creating a Series from a dictionary
    d = {"a": 100, "b": 200, "c": 300}
    s_dict = pd.Series(d)
    logger.info("\nSeries from dictionary:\n%s", s_dict)

if __name__ == "__main__":
    main()