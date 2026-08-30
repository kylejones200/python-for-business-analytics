"""Standardize features using StandardScaler.

This module demonstrates feature scaling for predictive maintenance data using
sklearn's StandardScaler. Readers learn the importance of feature normalization
for machine learning models and how to apply it to time series data.

Note: This preprocessing step should be part of a Pipeline when used with
train/test splits to prevent data leakage.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def main() -> None:
    """Standardize features using StandardScaler."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler

    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    try:
        from bookdata import ensure_dataset
    except ImportError:
        logger.error("Could not import bookdata module. Ensure src/bookdata.py exists.")
        raise SystemExit(1)

    # Load dataset
    ops_path = ensure_dataset("business_ops")
    if ops_path is None:
        logger.error("business_ops dataset unavailable. Run `python scripts/make_data.py`.")
        raise SystemExit(1)

    try:
        df = pd.read_parquet(ops_path)
        df["timestamp"] = pd.to_datetime(df["order_date"])
        df = df.set_index("timestamp").sort_index()
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

    # Define features
    features = [
        "gearbox_vibration",
        "generator_vibration",
        "tower_vibration",
        "humidity",
        "pressure",
        "temperature",
        "voltage",
        "power",
    ]

    # Validate columns exist
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        logger.warning(
            "Missing feature columns %s; generating synthetic signals for demo.", missing_features
        )
        rng = np.random.default_rng(42)
        t = np.arange(len(df), dtype=float)

        baseline = 2.0 + 0.2 * np.sin(t / 30.0) + 0.1 * np.cos(t / 17.0)
        df["gearbox_vibration"] = baseline + rng.normal(0, 0.15, len(df))
        df["generator_vibration"] = (baseline * 0.9) + rng.normal(0, 0.12, len(df))
        df["tower_vibration"] = (baseline * 0.7) + rng.normal(0, 0.10, len(df))

        df["temperature"] = 20.0 + 5.0 * np.sin(t / 40.0) + rng.normal(0, 0.8, len(df))
        df["humidity"] = 55.0 + 10.0 * np.cos(t / 55.0) + rng.normal(0, 2.5, len(df))
        df["pressure"] = 1013.0 + 3.0 * np.sin(t / 70.0) + rng.normal(0, 0.9, len(df))

        voltage = 480.0 + 8.0 * np.sin(t / 45.0) + rng.normal(0, 2.0, len(df))
        current = 15.0 + 1.8 * np.cos(t / 60.0) + rng.normal(0, 0.6, len(df))
        df["voltage"] = voltage
        df["power"] = (voltage * current) / 1000.0  # kW

    # Create training dataset (for demonstration - in practice would use Pipeline)
    df_train = df[features].copy()

    # Standardize features (mean=0, std=1)
    # NOTE: In production, this should be in a Pipeline fitted only on training data
    scaler = StandardScaler()
    df_train_scaled = pd.DataFrame(
        scaler.fit_transform(df_train), columns=features, index=df_train.index
    )

    logger.info("Feature scaling complete")
    logger.info("\nScaled feature statistics:")
    logger.info(f"\n{df_train_scaled.describe()}")

if __name__ == "__main__":
    main()
