"""

This script demonstrates creating heatmaps to visualize two-dimensional data patterns.
Readers learn to use color intensity to represent values in a matrix format.
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
    """Create heatmap visualization."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module

    # Set style
    set_minimalist_style()

    # Generate realistic temporal data
    np.random.seed(101)
    dates = pd.date_range("2023-01-01", periods=365, freq="D")
    values = 100 + np.random.normal(0, 20, 365)

    # Add day-of-week and monthly patterns
    df = pd.DataFrame({"Date": dates, "Value": values})
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["Month"] = df["Date"].dt.month
    df["Hour"] = np.random.randint(0, 24, 365)

    # Create pivot table
    pivot = df.pivot_table(
        values="Value", index="DayOfWeek", columns="Month", aggfunc="mean"
    )

    # Reorder days
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    pivot = pivot.reindex(day_order)

    # Create heatmap with matplotlib (no seaborn dependency)
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(pivot.values, cmap="RdYlGn", aspect="auto")

    # Set ticks and labels
    ax.set_xticks(np.arange(pivot.shape[1]))
    ax.set_yticks(np.arange(pivot.shape[0]))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticklabels(pivot.index)

    # Add values in cells (similar to seaborn annot=True)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            ax.text(
                j,
                i,
                f"{pivot.values[i, j]:.0f}",
                ha="center",
                va="center",
                fontsize=8,
                color="#2E3440",
            )

    # Cell boundary gridlines
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks(np.arange(pivot.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(pivot.shape[0] + 1) - 0.5, minor=True)
    
    ax.tick_params(which="minor", bottom=False, left=False)

    # Labels and title
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Day of Week", fontsize=11)
    ax.set_title("Average Values by Day of Week and Month", fontsize=13, pad=15)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Average Value", rotation=270, labelpad=20, fontsize=10)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_heatmap.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_heatmap.png'}")

if __name__ == "__main__":
    main()
