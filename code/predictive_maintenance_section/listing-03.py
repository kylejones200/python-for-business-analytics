"""Visualize environmental sensor measurements over time.

This module demonstrates plotting time series data for environmental sensors
(humidity, pressure, temperature) to identify patterns and correlations.
Readers learn how to visualize ambient conditions in predictive maintenance.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def main() -> None:
    """Plot environmental sensor measurements."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

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

    try:
        df = pd.read_parquet(ops_path)
        df["timestamp"] = pd.to_datetime(df["order_date"])
        df = df.set_index("timestamp").sort_index()
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

    # Environmental sensors
    ambient_sensors = ["humidity", "pressure", "temperature"]

    # Validate columns exist
    missing_sensors = [s for s in ambient_sensors if s not in df.columns]
    if missing_sensors:
        logger.warning(
            "Missing sensor columns %s; generating synthetic signals for demo.", missing_sensors
        )
        rng = np.random.default_rng(42)
        t = np.arange(len(df), dtype=float)
        df["temperature"] = 20.0 + 5.0 * np.sin(t / 40.0) + rng.normal(0, 0.8, len(df))
        df["humidity"] = 55.0 + 10.0 * np.cos(t / 55.0) + rng.normal(0, 2.5, len(df))
        df["pressure"] = 1013.0 + 3.0 * np.sin(t / 70.0) + rng.normal(0, 0.9, len(df))

    fig, ax = plt.subplots(figsize=(14, 6))
    df[ambient_sensors].plot(ax=ax, alpha=0.7)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Measurement Value", fontsize=12)
    ax.set_title("Environmental Conditions Over Time", fontsize=14)
    ax.legend(loc="upper right")
    
    plt.tight_layout()

    # Save plot before showing
    output_path = ROOT / "img" / "predictive_maintenance_environmental.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    import os

if __name__ == "__main__":
    main()
