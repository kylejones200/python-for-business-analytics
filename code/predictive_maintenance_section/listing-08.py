"""Analyze feature correlations in preprocessed sensor data.

This module demonstrates calculating and visualizing correlation matrices to
identify highly correlated features. Readers learn how to detect multicollinearity
and redundant features in predictive maintenance data.

"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def main() -> None:
    """Calculate and visualize feature correlations."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
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

    # Calculate correlation matrix
    corr_matrix = df_train_scaled.corr()

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix), k=1)  # Mask upper triangle
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        mask=mask,
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )
    ax.set_title("Feature Correlation Matrix", fontsize=14, pad=15)
    plt.tight_layout()

    # Save plot before showing
    output_path = ROOT / "img" / "predictive_maintenance_correlation.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Plot saved to {output_path}")
    import os

    # Identify highly correlated features
    threshold = 0.8
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                high_corr.append(
                    {
                        "feature1": corr_matrix.columns[i],
                        "feature2": corr_matrix.columns[j],
                        "correlation": corr_matrix.iloc[i, j],
                    }
                )

    if high_corr:
        logger.info(f"\nHighly correlated features (|r| > {threshold}):")
        for pair in high_corr:
            logger.info(
                f"{pair['feature1']} <-> {pair['feature2']}: {pair['correlation']:.3f}"
            )
    else:
        logger.info(f"\nNo features with correlation > {threshold} found")

if __name__ == "__main__":
    main()
