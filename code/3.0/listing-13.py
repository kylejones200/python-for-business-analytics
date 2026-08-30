"""

This script demonstrates seasonal decomposition of time series data. Readers
learn to decompose time series into trend, seasonal, and residual components.
"""

import logging
import os
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import minimalist_style
from minimalist_style import set_minimalist_style
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def main():
    """Perform seasonal decomposition and visualize components."""
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s: %(message)s'
    )
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    # Set style
    set_minimalist_style()

    # Generate time series with clear components
    np.random.seed(789)
    dates = pd.date_range("2023-01-01", periods=365, freq="D")
    trend = np.linspace(100, 200, 365)
    seasonal = 20 * np.sin(2 * np.pi * np.arange(365) / 30)  # 30-day cycle
    residual = np.random.normal(0, 5, 365)
    values = trend + seasonal + residual

    df = pd.DataFrame({"Date": dates, "Value": values})
    df.set_index("Date", inplace=True)

    # Perform seasonal decomposition
    decomposed = seasonal_decompose(df["Value"], model="additive", period=30)

    # Create subplots
    fig, axes = plt.subplots(4, 1, figsize=(12, 10))

    # Original data
    axes[0].plot(df.index, df["Value"], color="#2E3440", linewidth=1)
    remove_chartjunk(axes[0])
    axes[0].set_ylabel("Observed", fontsize=10)
    axes[0].set_title(
        "Seasonal Decomposition of Time Series", fontsize=13, pad=10
    )

    # Trend
    axes[1].plot(df.index, decomposed.trend, color="#5E81AC", linewidth=2)
    remove_chartjunk(axes[1])
    axes[1].set_ylabel("Trend", fontsize=10)

    # Seasonal
    axes[2].plot(
        df.index, decomposed.seasonal, color="#A3BE8C", linewidth=1.5
    )
    remove_chartjunk(axes[2])
    axes[2].set_ylabel("Seasonal", fontsize=10)

    # Residual
    axes[3].plot(
        df.index, decomposed.resid, color="#BF616A", linewidth=0.8, alpha=0.7
    )
    axes[3].axhline(
        0, color="#4C566A", linestyle="--", linewidth=1, alpha=0.5
    )
    remove_chartjunk(axes[3])
    axes[3].set_ylabel("Residual", fontsize=10)
    axes[3].set_xlabel("Date", fontsize=11)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(
        img_dir / "ch3_seasonal_decomposition.png",
        dpi=150,
        bbox_inches="tight",
    )
    logger.info(
        f"Saved figure to {img_dir / 'ch3_seasonal_decomposition.png'}"
    )

    # Log component statistics
    logger.info("\nComponent Statistics:")
    logger.info(
        f"Trend range: {decomposed.trend.min():.2f} to "
        f"{decomposed.trend.max():.2f}"
    )
    logger.info(f"Seasonal amplitude: {decomposed.seasonal.max():.2f}")
    logger.info(f"Residual std dev: {decomposed.resid.std():.2f}")


if __name__ == "__main__":
    main()
