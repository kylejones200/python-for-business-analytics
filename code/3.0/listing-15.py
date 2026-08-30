"""

This script demonstrates creating multi-panel dashboards with shared axes.
Readers learn to create coordinated visualizations that share time axes.
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
    """Create multi-panel dashboard with shared axes."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    # Set style
    set_minimalist_style()

    # Generate multiple related time series
    np.random.seed(202)
    dates = pd.date_range("2023-01-01", periods=100, freq="D")

    series_data = {
        "Revenue": 100 + 2 * np.arange(100) + np.random.normal(0, 10, 100),
        "Costs": 60 + 1.5 * np.arange(100) + np.random.normal(0, 8, 100),
        "Customers": 1000 + 10 * np.arange(100) + np.random.normal(0, 50, 100),
        "Satisfaction": 7 + 0.01 * np.arange(100) + np.random.normal(0, 0.3, 100),
    }

    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    fig.suptitle("Business Metrics Dashboard", fontsize=15, y=0.995)

    colors = ["#5E81AC", "#A3BE8C", "#D08770", "#B48EAD"]

    for ax, (name, values), color in zip(axes.flat, series_data.items(), colors):
        ax.plot(
            dates,
            values,
            color=color,
            linewidth=2,
            marker="o",
            markersize=3,
            markerfacecolor="white",
            markeredgewidth=1.5,
            markeredgecolor=color,
        )

        # Add trend line
        z = np.polyfit(range(len(values)), values, 1)
        p = np.poly1d(z)
        ax.plot(
            dates,
            p(range(len(values))),
            color="#2E3440",
            linestyle="--",
            linewidth=1.5,
            alpha=0.5,
        )

        remove_chartjunk(ax)
        ax.set_ylabel(name, fontsize=10, color=color, fontweight="bold")
        ax.set_title(name, fontsize=11, pad=8)

        # Add growth rate annotation
        growth = ((values[-1] - values[0]) / values[0]) * 100
        ax.text(
            0.02,
            0.98,
            f"{growth:+.1f}%",
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7, edgecolor="none"),
        )

    # Set x-label only for bottom plots
    for ax in axes[1, :]:
        ax.set_xlabel("Date", fontsize=10)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=8)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_metrics_dashboard.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_metrics_dashboard.png'}")

if __name__ == "__main__":
    main()
