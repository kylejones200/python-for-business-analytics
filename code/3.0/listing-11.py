"""

This script demonstrates creating horizontal box plots with custom styling.
Readers learn to visualize distributions across categories and add value
annotations.
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

logger = logging.getLogger(__name__)


def main():
    """Create horizontal box plot with value annotations."""
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s: %(message)s'
    )
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    # Set style
    set_minimalist_style()

    # Generate data for different products
    np.random.seed(123)
    product_data = {
        "Premium Widget": np.random.normal(95, 10, 100),
        "Standard Widget": np.random.normal(80, 12, 100),
        "Economy Widget": np.random.normal(65, 15, 100),
        "Budget Widget": np.random.normal(50, 8, 100),
    }

    # Create horizontal box plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Prepare data
    data_list = list(product_data.values())
    labels = list(product_data.keys())

    # Create box plot
    bp = ax.boxplot(
        data_list,
        tick_labels=labels,
        patch_artist=True,
        vert=False,
        boxprops=dict(facecolor="#5E81AC", alpha=0.3, linewidth=1),
        medianprops=dict(color="#2E3440", linewidth=2),
        whiskerprops=dict(color="#4C566A", linewidth=1),
        capprops=dict(color="#4C566A", linewidth=1),
        flierprops=dict(
            marker="o",
            markerfacecolor="#5E81AC",
            markersize=4,
            alpha=0.5,
            linestyle="none",
        ),
    )

    # Remove chartjunk
    remove_chartjunk(ax)

    # Add labels
    ax.set_xlabel("Customer Satisfaction Score", fontsize=11)
    ax.set_title("Product Satisfaction by Tier", fontsize=13, pad=15)

    # Add median values as text
    for i, (product, values) in enumerate(product_data.items()):
        median = np.median(values)
        ax.text(
            median,
            i + 1,
            f" {median:.1f}",
            va="center",
            ha="left",
            fontsize=9,
            color="#2E3440",
            fontweight="bold",
        )

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(
        img_dir / "ch3_product_satisfaction.png", dpi=150, bbox_inches="tight"
    )
    logger.info(f"Saved figure to {img_dir / 'ch3_product_satisfaction.png'}")


if __name__ == "__main__":
    main()
