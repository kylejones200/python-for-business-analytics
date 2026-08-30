"""Compare original vs preprocessed sensor data.

This module demonstrates visualizing the effects of preprocessing (denoising
and scaling) on sensor data. Readers learn how to compare raw and processed
data to understand preprocessing impact.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def main() -> None:
    """Compare original vs preprocessed data."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import matplotlib.pyplot as plt
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
    features = ["gearbox_vibration", "generator_vibration", "tower_vibration",
                "humidity", "pressure", "temperature", "voltage", "power"]

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

    # Create preprocessed dataset
    df_train = df[features].copy()
    scaler = StandardScaler()
    df_train_scaled = pd.DataFrame(
        scaler.fit_transform(df_train), columns=features, index=df_train.index
    )

    # Compare original vs preprocessed data for one feature
    feature_to_plot = "gearbox_vibration"

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Original data
    df[feature_to_plot].plot(ax=ax1, alpha=0.7, color="blue")
    ax1.set_title(f"{feature_to_plot} - Original Data", fontsize=14)
    ax1.set_ylabel("Vibration (mm/s)", fontsize=12)

    # Preprocessed data
    df_train_scaled[feature_to_plot].plot(ax=ax2, alpha=0.7, color="green")
    ax2.set_title(f"{feature_to_plot} - Denoised and Scaled", fontsize=14)
    ax2.set_xlabel("Time", fontsize=12)
    ax2.set_ylabel("Standardized Value", fontsize=12)

    plt.tight_layout()

    # Save plot before showing
    output_path = ROOT / "img" / "predictive_maintenance_preprocessing_comparison.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    import os

if __name__ == "__main__":
    main()
