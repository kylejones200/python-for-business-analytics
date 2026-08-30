"""Create sliding window sequences from time series data.

This module demonstrates creating sequences from time series data for use with
sequence models (LSTM, GRU, etc.). Readers learn how to prepare time series
data for deep learning models using sliding windows.

Note: When using these sequences for modeling, ensure time-aware train/test
splits to prevent temporal leakage. Sequences should be split chronologically,
not randomly shuffled.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def create_sequences(data, time_steps=100, step=10):
    """Create sliding window sequences from time series data.

    Args:
        data: DataFrame with sensor readings (time-indexed).
        time_steps: Length of each sequence (lookback window).
        step: Step size between sequences (overlap control).

    Returns:
        numpy.ndarray: 3D array of shape (n_sequences, time_steps, n_features).
    """
    import numpy as np

    if len(data) < time_steps:
        raise ValueError(f"Data length ({len(data)}) must be >= time_steps ({time_steps})")

    sequences = []
    for i in range(0, len(data) - time_steps, step):
        sequence = data.iloc[i : (i + time_steps)].values
        sequences.append(sequence)

    return np.array(sequences)

def main() -> None:
    """Create sequences from preprocessed sensor data."""
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

    # Create sequences
    INTERVAL = 5  # 5-minute intervals in your data
    TIME_STEPS = 20 * INTERVAL  # 100 time steps (500 minutes = ~8 hours)
    STEP = 10  # Overlap sequences by 90%

    X_sequences = create_sequences(df_train_scaled, TIME_STEPS, STEP)

    logger.info(f"Sequence shape: {X_sequences.shape}")
    logger.info(f"  - Number of sequences: {X_sequences.shape[0]}")
    logger.info(f"  - Time steps per sequence: {X_sequences.shape[1]}")
    logger.info(f"  - Number of features: {X_sequences.shape[2]}")

if __name__ == "__main__":
    main()
