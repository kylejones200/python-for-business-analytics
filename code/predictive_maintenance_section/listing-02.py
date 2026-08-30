"""Visualize vibration sensor measurements over time.

This module demonstrates plotting time series data for vibration sensors to
identify patterns and anomalies. Readers learn how to visualize sensor data
for exploratory analysis in predictive maintenance.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def main():
    """Plot vibration sensor measurements."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

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

    if not Path(ops_path).exists():
        logger.error(f"Dataset file not found: {ops_path}")
        raise SystemExit(1)

    try:
        df = pd.read_parquet(ops_path)
        df["timestamp"] = pd.to_datetime(df["order_date"])
        df = df.set_index("timestamp").sort_index()
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

    # Define sensor groups
    vibration_sensors = ["gearbox_vibration", "generator_vibration", "tower_vibration"]

    # Validate columns exist
    missing_sensors = [s for s in vibration_sensors if s not in df.columns]
    if missing_sensors:
        logger.warning("Missing sensor columns %s; generating synthetic signals for demo.", missing_sensors)
        rng = np.random.default_rng(42)
        t = np.arange(len(df), dtype=float)
        baseline = 2.0 + 0.2 * np.sin(t / 30.0) + 0.1 * np.cos(t / 17.0)
        df["gearbox_vibration"] = baseline + rng.normal(0, 0.15, len(df))
        df["generator_vibration"] = (baseline * 0.9) + rng.normal(0, 0.12, len(df))
        df["tower_vibration"] = (baseline * 0.7) + rng.normal(0, 0.10, len(df))
        # Inject a small anomaly window.
        if len(df) > 200:
            df.iloc[150:175, df.columns.get_loc("gearbox_vibration")] += 0.8

    # Plot vibration data
    fig, ax = plt.subplots(figsize=(14, 6))
    df[vibration_sensors].plot(ax=ax, alpha=0.7)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Vibration (mm/s)", fontsize=12)
    ax.set_title("Vibration Measurements Over Time", fontsize=14)
    ax.legend(loc="upper right")
    plt.tight_layout()

    # Save plot before showing
    output_path = ROOT / "img" / "predictive_maintenance_vibration.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    import os

if __name__ == "__main__":
    main()
