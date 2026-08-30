"""

This script demonstrates calculating and visualizing moving averages on time series data.
Readers learn to smooth time series data and identify trends using different window sizes.
"""
import logging
import os
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import minimalist_style
from minimalist_style import set_minimalist_style
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def main():
    """Create time series plot with multiple moving averages."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    # Set style
    set_minimalist_style()

    # Generate time series with trend and noise
    np.random.seed(456)
    dates = pd.date_range("2023-01-01", periods=100, freq="D")
    base = 100
    trend = 2 * np.arange(100)
    seasonality = 15 * np.sin(np.linspace(0, 10, 100))
    noise = np.random.normal(0, 5, 100)
    values = base + trend + seasonality + noise

    df = pd.DataFrame({"Date": dates, "Value": values})

    # Calculate moving averages of different windows
    df["MA_7"] = df["Value"].rolling(window=7).mean()
    df["MA_14"] = df["Value"].rolling(window=14).mean()
    df["MA_30"] = df["Value"].rolling(window=30).mean()

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot original data with low alpha
    ax.plot(
        df["Date"],
        df["Value"],
        label="Original Data",
        alpha=0.4,
        linewidth=1,
        color="#4C566A",
    )

    # Plot moving averages
    ax.plot(df["Date"], df["MA_7"], label="7-Day MA", linewidth=2, color="#5E81AC")
    ax.plot(df["Date"], df["MA_14"], label="14-Day MA", linewidth=2, color="#A3BE8C")
    ax.plot(df["Date"], df["MA_30"], label="30-Day MA", linewidth=2.5, color="#BF616A")

    # Formatting
    remove_chartjunk(ax)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Value", fontsize=11)
    ax.set_title("Time Series with Multiple Moving Averages", fontsize=13, pad=15)
    ax.legend(frameon=False, loc="upper left")

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_moving_averages.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_moving_averages.png'}")

if __name__ == "__main__":
    main()
