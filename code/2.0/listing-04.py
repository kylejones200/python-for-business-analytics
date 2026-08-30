"""Demonstrates loading data from parquet files using the bookdata module.

This script shows how to load datasets using the ensure_dataset utility function.
Readers learn data loading patterns, parquet file handling, and dataset
management utilities.

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 04
"""
import logging
import sys
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating data loading."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    try:
        from bookdata import ensure_dataset
    except ImportError:
        logger.error("bookdata module not found. Ensure src/bookdata.py exists.")
        raise SystemExit(1)

    customers_path = ensure_dataset("business_customers")
    if customers_path is None:
        logger.warning("SKIPPED: business_customers dataset unavailable. Run `python scripts/make_data.py`.")
        raise SystemExit(0)

    df_customers = pd.read_parquet(customers_path)
    logger.info(df_customers.head())

if __name__ == "__main__":
    main()