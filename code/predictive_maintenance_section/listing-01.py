"""Load and explore predictive maintenance time series dataset.

This module demonstrates loading time-indexed operational data for predictive
maintenance analysis. Readers learn how to load time series data, set datetime
indexes, and perform initial data exploration.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def main():
    """Load and explore predictive maintenance dataset."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    import numpy as np  # noqa: F401
    import pandas as pd

    # Optional imports (used in later, notebook-style listings).
    try:
        import matplotlib.pyplot as plt  # noqa: F401
        import seaborn as sns  # noqa: F401
        from sklearn.preprocessing import StandardScaler  # noqa: F401
        import pywt  # noqa: F401
    except Exception:
        pass

    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    try:
        from bookdata import ensure_dataset
    except ImportError:
        logger.error("Could not import bookdata module. Ensure src/bookdata.py exists.")
        raise SystemExit(1)

    # Load a local, reproducible operational dataset.
    ops_path = ensure_dataset("business_ops")
    if ops_path is None:
        logger.error("business_ops dataset unavailable. Run `python scripts/make_data.py`.")
        raise SystemExit(1)

    if not Path(ops_path).exists():
        logger.error(f"Dataset file not found: {ops_path}")
        raise SystemExit(1)

    try:
        df = pd.read_parquet(ops_path)
    except Exception as e:
        logger.error(f"Error reading parquet file: {e}")
        raise

    if df.empty:
        logger.error("Dataset is empty")
        raise SystemExit(1)

    if "order_date" not in df.columns:
        logger.error("Dataset missing required 'order_date' column")
        raise SystemExit(1)

    df["timestamp"] = pd.to_datetime(df["order_date"])
    df = df.set_index("timestamp").sort_index()

    # Display basic information
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"Date range: {df.index.min()} to {df.index.max()}")
    logger.info(f"\nColumns: {df.columns.tolist()}")
    logger.info(f"\nFirst few rows:")
    logger.info(f"\n{df.head()}")

    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        logger.warning(f"\nMissing values:\n{missing[missing > 0]}")
    else:
        logger.info("\nNo missing values found")

if __name__ == "__main__":
    main()
