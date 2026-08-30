"""

This script demonstrates creating small multiples (facet plots) for comparing multiple series.
Readers learn to create grid layouts of similar plots for easy comparison.
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
    """Create small multiples visualization."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    # Set style
    set_minimalist_style()

    # Example: Monthly sales trends for 6 products
    np.random.seed(404)
    months = np.arange(1, 13)
    products = [
        "Product A",
        "Product B",
        "Product C",
        "Product D",
        "Product E",
        "Product F",
    ]

    # Create 2x3 grid of small multiples
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharex=True, sharey=True)
    fig.suptitle("Monthly Sales Trends by Product", fontsize=14, y=0.995)

    # Flatten axes for iteration
    axes = axes.flatten()

    for idx, (ax, product) in enumerate(zip(axes, products)):
        # Generate different trend for each product
        trend = np.random.uniform(0.5, 2.0)
        seasonality = 5 * np.sin(months / 2)
        noise = np.random.normal(0, 2, 12)
        sales = 20 + trend * months + seasonality + noise

        # Plot
        ax.plot(months, sales, color="#5E81AC", linewidth=2, marker="o", markersize=4)
        ax.fill_between(months, sales, alpha=0.2, color="#5E81AC")

        # Formatting
        remove_chartjunk(ax)
        ax.set_title(product, fontsize=11, pad=8)
        ax.set_ylim(10, 50)

        # Only add labels to edge plots
        if idx >= 3:
            ax.set_xlabel("Month", fontsize=9)
        if idx % 3 == 0:
            ax.set_ylabel("Sales ($1000s)", fontsize=9)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_small_multiples.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_small_multiples.png'}")

if __name__ == "__main__":
    main()
