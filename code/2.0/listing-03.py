"""Demonstrates creating pandas DataFrames from different data structures.

This script shows how to create DataFrames from dictionaries, with custom
indexes, and from lists of dictionaries. Readers learn DataFrame creation,
indexing, and various data input formats.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 03
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating DataFrame creation."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Creating a DataFrame from a dictionary
    data = {
        "Name": ["John", "Anna", "Peter", "Linda"],
        "Age": [28, 34, 29, 32],
        "City": ["New York", "Paris", "Berlin", "London"],
    }
    df = pd.DataFrame(data)
    logger.info("DataFrame:\n%s", df)

    # Creating a DataFrame with custom index
    df_indexed = pd.DataFrame(data, index=["person1", "person2", "person3", "person4"])
    logger.info("\nDataFrame with custom index:\n%s", df_indexed)

    # Creating a DataFrame from a list of dictionaries
    data_list = [
        {"Name": "Tom", "Age": 25, "City": "Tokyo"},
        {"Name": "Emma", "Age": 31, "City": "Sydney"},
    ]
    df_list = pd.DataFrame(data_list)
    logger.info("\nDataFrame from list of dicts:\n%s", df_list)

if __name__ == "__main__":
    main()