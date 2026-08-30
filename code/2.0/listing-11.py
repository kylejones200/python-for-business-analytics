"""Demonstrates reshaping data from wide to long format using pd.melt().

This script shows how to convert wide-format data (multiple columns per
variable) to long format (one row per observation). Readers learn data
reshaping, melt() function, and tidy data principles.

"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating wide-to-long data reshaping."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Example: Convert quarterly sales from wide to long format
    # Wide format
    df_wide = pd.DataFrame(
        {
            "Product": ["A", "B", "C"],
            "Q1_Sales": [100, 150, 120],
            "Q2_Sales": [120, 160, 130],
            "Q3_Sales": [110, 170, 125],
            "Q4_Sales": [130, 180, 140],
        }
    )

    # Convert to long format
    df_long = pd.melt(
        df_wide, id_vars=["Product"], var_name="Quarter", value_name="Sales"
    )

    logger.info(df_long)

if __name__ == "__main__":
    main()
