"""Visualize electrical sensor measurements over time.

This module demonstrates plotting time series data for electrical sensors
(voltage, current, power) to identify patterns and anomalies. Readers learn
how to visualize electrical measurements in predictive maintenance.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def main() -> None:
    """Plot electrical sensor measurements."""
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

    # Electrical sensors
    electrical_sensors = ["voltage", "current", "power"]

    # Validate columns exist
    missing_sensors = [s for s in electrical_sensors if s not in df.columns]
    if missing_sensors:
        logger.warning(
            "Missing sensor columns %s; generating synthetic signals for demo.", missing_sensors
        )
        rng = np.random.default_rng(42)
        t = np.arange(len(df), dtype=float)
        voltage = 480.0 + 8.0 * np.sin(t / 45.0) + rng.normal(0, 2.0, len(df))
        current = 15.0 + 1.8 * np.cos(t / 60.0) + rng.normal(0, 0.6, len(df))
        power = (voltage * current) / 1000.0  # kW
        df["voltage"] = voltage
        df["current"] = current
        df["power"] = power

    fig, ax = plt.subplots(figsize=(14, 6))
    df[electrical_sensors].plot(ax=ax, alpha=0.7)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Measurement Value", fontsize=12)
    ax.set_title("Electrical Measurements Over Time", fontsize=14)
    ax.legend(loc="upper right")
    
    plt.tight_layout()

    # Save plot before showing
    output_path = ROOT / "img" / "predictive_maintenance_electrical.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    import os

if __name__ == "__main__":
    main()
