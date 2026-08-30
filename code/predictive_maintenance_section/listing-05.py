"""Apply wavelet denoising to time series sensor data.

This module demonstrates using wavelet transforms to denoise sensor readings
for predictive maintenance. Readers learn how to remove noise from time series
data while preserving important signal patterns.

Note: When used for modeling with train/test splits, this preprocessing should
be wrapped in a Pipeline to prevent data leakage.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def wavelet_denoise(data, wavelet="db6", level=None):
    """Denoise time series data using wavelet transform.

    Args:
        data: 1D array of sensor readings.
        wavelet: Wavelet family (db6 is good for sensor data).
        level: Decomposition level (None for automatic).

    Returns:
        numpy.ndarray: Denoised 1D array.
    """
    import numpy as np
    import pywt

    if len(data) == 0:
        raise ValueError("Input data cannot be empty")

    # Compute wavelet coefficients
    coeff = pywt.wavedec(data, wavelet, level=level)

    # Calculate threshold using universal threshold
    sigma = np.median(np.abs(coeff[-1])) / 0.6745
    threshold = sigma * np.sqrt(2 * np.log(len(data)))

    # Apply soft thresholding
    coeff_thresholded = [pywt.threshold(c, threshold, mode="soft") for c in coeff]

    # Reconstruct signal
    denoised = pywt.waverec(coeff_thresholded, wavelet)

    # Handle length mismatch due to wavelet transform
    return denoised[: len(data)]

def main() -> None:
    """Apply wavelet denoising to sensor features."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import numpy as np
    import pandas as pd

    try:
        import pywt  # noqa: F401
    except ImportError:
        logger.error(
            "PyWavelets is not installed. Install with: pip install PyWavelets"
        )
        raise SystemExit(1)

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

    # Define features to process
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
        logger.warning("Missing feature columns %s; generating synthetic signals for demo.", missing_features)
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

    # Create training dataset
    df_train = df[features].copy()

    # Apply wavelet denoising to each feature
    logger.info("Applying wavelet denoising...")
    raw_std = df_train.std()
    for feature in features:
        df_train[feature] = wavelet_denoise(df_train[feature].values, "db6")
        logger.info(f"Denoised: {feature}")

    denoised_std = df_train.std()
    logger.info("Std dev (raw -> denoised) for first 3 features:\n%s", pd.DataFrame({"raw": raw_std, "denoised": denoised_std}).head(3))

if __name__ == "__main__":
    main()
