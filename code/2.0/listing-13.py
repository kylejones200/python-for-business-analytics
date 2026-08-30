"""Demonstrates converting DataFrame column data types.

This script shows how to convert columns to datetime, category, and numeric
types. Readers learn data type conversion, pd.to_datetime(), pd.to_numeric(),
and astype() methods.

"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating data type conversion."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Create example DataFrame
    import pandas as pd
    df = pd.DataFrame({
        'Date': ['2023-01-01', '2023-02-01', '2023-03-01'],
        'Region': ['North', 'South', 'East'],
        'Sales': ['100', '200', '300']
    })
    
    # Example: Convert data types
    df["Date"] = pd.to_datetime(df["Date"])
    df["Region"] = df["Region"].astype("category")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    logger.info("Data types converted successfully")
    logger.info(f"Date column type: {df['Date'].dtype}")
    logger.info(f"Region column type: {df['Region'].dtype}")
    logger.info(f"Sales column type: {df['Sales'].dtype}")

if __name__ == "__main__":
    main()
