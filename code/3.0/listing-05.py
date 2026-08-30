"""

This script demonstrates creating time series line plots with annotations.
Readers learn to visualize temporal trends and highlight key data points.
"""

import logging
import os
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import minimalist_style
from minimalist_style import set_minimalist_style
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Create time series line plot with annotations."""
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s: %(message)s'
    )
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    # Set style
    set_minimalist_style()

    # Example: Monthly revenue with seasonal pattern
    months = pd.date_range("2023-01-01", periods=24, freq="ME")
    month_labels = [m.strftime("%b %y") for m in months]

    # Create realistic seasonal data
    np.random.seed(789)
    base_revenue = 100
    trend = np.linspace(0, 40, 24)  # Upward trend
    seasonal = 15 * np.sin(np.linspace(0, 4 * np.pi, 24))  # Seasonal pattern
    noise = np.random.normal(0, 5, 24)
    revenue = base_revenue + trend + seasonal + noise

    # Create line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        range(24),
        revenue,
        color="#5E81AC",
        linewidth=2.5,
        marker="o",
        markersize=5,
        markerfacecolor="white",
        markeredgewidth=2,
        markeredgecolor="#5E81AC",
    )

    # Highlight key points
    max_idx = np.argmax(revenue)
    min_idx = np.argmin(revenue)
    ax.scatter(
        [max_idx, min_idx],
        [revenue[max_idx], revenue[min_idx]],
        color="#BF616A",
        s=100,
        zorder=5,
        edgecolors="white",
        linewidth=2,
    )

    # Annotations
    ax.annotate(
        f"Peak\n${revenue[max_idx]:.0f}K",
        xy=(max_idx, revenue[max_idx]),
        xytext=(max_idx + 1, revenue[max_idx] + 5),
        fontsize=9,
        color="#2E3440",
        arrowprops=dict(arrowstyle="->", color="#4C566A", lw=1),
    )

    ax.annotate(
        f"Low\n${revenue[min_idx]:.0f}K",
        xy=(min_idx, revenue[min_idx]),
        xytext=(min_idx + 1, revenue[min_idx] - 8),
        fontsize=9,
        color="#2E3440",
        arrowprops=dict(arrowstyle="->", color="#4C566A", lw=1),
    )

    # Formatting
    remove_chartjunk(ax)
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Revenue ($1000s)", fontsize=11)
    ax.set_title(
        "Monthly Revenue: 2-Year Trend with Seasonality", fontsize=13, pad=15
    )
    ax.set_xticks(range(0, 24, 3))
    ax.set_xticklabels(
        [month_labels[i] for i in range(0, 24, 3)], rotation=45, ha="right"
    )

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(
        img_dir / "ch3_revenue_trend.png", dpi=150, bbox_inches="tight"
    )
    logger.info(f"Saved figure to {img_dir / 'ch3_revenue_trend.png'}")


if __name__ == "__main__":
    main()
