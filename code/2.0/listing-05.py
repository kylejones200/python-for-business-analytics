"""Demonstrates loading business operations data from parquet files.

This script shows how to load the business_ops dataset using the ensure_dataset
utility. Readers learn dataset loading, parquet file handling, and data
exploration with head().

Chapter: Understanding Data Before Modeling
Source: 2.0.tex
Extracted listing: 05
"""
import logging
import sys
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating business operations data loading."""
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

    ops_path = ensure_dataset("business_ops")
    if ops_path is None:
        logger.warning("SKIPPED: business_ops dataset unavailable. Run `python scripts/make_data.py`.")
        raise SystemExit(0)

    df_ops = pd.read_parquet(ops_path)
    logger.info(df_ops.head())

if __name__ == "__main__":
    main()