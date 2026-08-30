"""Demonstrates reshaping data from long to wide format using pivot().

This script shows how to convert long-format data back to wide format using
the pivot() method. Readers learn data reshaping in both directions, pivot
operations, and index/column/value specifications.

"""

import logging

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating long-to-wide data reshaping."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Create example long-format data
    import pandas as pd

    df_long = pd.DataFrame(
        {
            'Product': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
            'Quarter': ['Q1_Sales', 'Q2_Sales', 'Q3_Sales', 'Q4_Sales'] * 2,
            'Sales': [100, 120, 110, 130, 150, 160, 170, 180],
        }
    )

    # Convert back to wide format
    df_wide_again = df_long.pivot(
        index="Product", columns="Quarter", values="Sales"
    )
    logger.info("Reshaped to wide format:\n%s", df_wide_again)


if __name__ == "__main__":
    main()
