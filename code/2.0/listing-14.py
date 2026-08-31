"""Demonstrates advanced missing data handling techniques.

This script shows various strategies for handling missing data including
selective dropping, mean imputation, and forward/backward filling for time
series. Readers learn different imputation strategies and when to use each.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 14
"""

import logging

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating advanced missing data handling."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Create example DataFrame with missing values
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    df = pd.DataFrame(
        {
            'Date': dates,
            'Sales': [
                100,
                np.nan,
                120,
                np.nan,
                110,
                130,
                np.nan,
                140,
                150,
                160,
            ],
            'Income': [
                1000,
                1200,
                np.nan,
                1400,
                1500,
                np.nan,
                1700,
                1800,
                1900,
                2000,
            ],
        }
    )

    # Drop rows with any missing values
    df_clean = df.dropna()
    logger.info(
        f"Dropped {len(df) - len(df_clean)} rows with any missing values"
    )

    # Drop rows where specific columns have missing values
    df_clean = df.dropna(subset=["Sales", "Date"])
    logger.info(
        f"Dropped {len(df) - len(df_clean)} rows with missing Sales or Date"
    )

    # Impute with mean or median
    if "Income" in df.columns:
        df["Income"].fillna(df["Income"].mean(), inplace=True)
        logger.info("Income missing values filled with mean")

    # Forward-fill or backward-fill for time series
    if "Sales" in df.columns:
        df["Sales"].ffill(inplace=True)  # Forward fill
        df["Sales"].bfill(inplace=True)  # Backward fill
        logger.info("Sales missing values filled with forward/backward fill")

    # Check for missing values
    logger.info("Missing values after imputation:\n%s", df.isnull().sum())


if __name__ == "__main__":
    main()
