"""Demonstrates dropping columns with high missing value percentages.

This script shows how to identify and remove columns that exceed a missing
value threshold. Readers learn threshold-based column removal, missing value
analysis, and data quality assessment.

"""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Drop columns whose share of missing values exceeds a threshold."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Load or create example data with missing values
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    try:
        from bookdata import ensure_dataset

        ops_path = ensure_dataset("business_ops")
        if ops_path:
            df = pd.read_parquet(ops_path)[
                [
                    "order_date",
                    "quantity",
                    "unit_price_usd",
                    "discount_rate",
                    "net_value_usd",
                    "satisfaction",
                ]
            ].copy()
            # Create artificial missingness for demonstration
            np.random.seed(42)
            df.loc[10:250, "satisfaction"] = np.nan
            df.loc[100:175, "discount_rate"] = np.nan
            # Make one column have >50% missing
            df.loc[: int(len(df) * 0.6), "satisfaction"] = np.nan
        else:
            np.random.seed(42)
            df = pd.DataFrame(
                {
                    'col1': np.random.normal(0, 1, 500),
                    'col2': np.random.normal(0, 1, 500),
                    'col3': np.random.normal(0, 1, 500),
                }
            )
            df.loc[: int(len(df) * 0.6), "col1"] = np.nan
    except ImportError:
        np.random.seed(42)
        df = pd.DataFrame(
            {
                'col1': np.random.normal(0, 1, 500),
                'col2': np.random.normal(0, 1, 500),
                'col3': np.random.normal(0, 1, 500),
            }
        )
        df.loc[: int(len(df) * 0.6), "col1"] = np.nan

    # Drop columns with > 50% missing
    threshold = 0.5
    missing_pct = df.isnull().sum() / len(df)
    columns_to_drop = missing_pct[missing_pct > threshold].index

    df_column_dropped = df.drop(columns=columns_to_drop)
    logger.info(f"Dropped columns: {list(columns_to_drop)}")
    logger.info(
        f"Original shape: {df.shape}, After dropping: "
        f"{df_column_dropped.shape}"
    )


if __name__ == "__main__":
    main()
