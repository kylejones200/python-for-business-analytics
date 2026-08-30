"""Demonstrates dropping rows with missing values and analyzing data loss.

This script shows how to remove rows with missing values and calculate the
impact on data size. Readers learn data cleaning, missing value handling,
and assessing data loss from cleaning operations.

"""
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating row dropping with missing values."""
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
        else:
            # Create synthetic data with missing values
            np.random.seed(42)
            df = pd.DataFrame({
                'col1': np.random.normal(0, 1, 500),
                'col2': np.random.normal(0, 1, 500),
                'col3': np.random.normal(0, 1, 500),
            })
            df.loc[10:250, "col1"] = np.nan
            df.loc[100:175, "col2"] = np.nan
    except ImportError:
        np.random.seed(42)
        df = pd.DataFrame({
            'col1': np.random.normal(0, 1, 500),
            'col2': np.random.normal(0, 1, 500),
            'col3': np.random.normal(0, 1, 500),
        })
        df.loc[10:250, "col1"] = np.nan
        df.loc[100:175, "col2"] = np.nan
    
    # Drop rows with any missing values
    df_dropped = df.dropna()
    
    logger.info(f"Original shape: {df.shape}")
    logger.info(f"After dropping rows: {df_dropped.shape}")
    logger.info(
        f"Rows lost: {df.shape[0] - df_dropped.shape[0]} "
        f"({(df.shape[0] - df_dropped.shape[0]) / df.shape[0] * 100:.1f}%)"
    )

if __name__ == "__main__":
    main()
