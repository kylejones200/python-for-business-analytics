"""

This script demonstrates overlaying theoretical distributions on histograms.
Readers learn to compare empirical data distributions with theoretical models.
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
    """Create histogram with theoretical distribution overlay."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    # Set style
    set_minimalist_style()

    # Generate normal distribution data
    np.random.seed(42)
    mu, sigma = 0, 1
    data = np.random.normal(mu, sigma, 1000)

    # Create histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    count, bins, ignored = ax.hist(
        data, bins=30, density=True, alpha=0.5, color="#5E81AC", edgecolor="white"
    )

    # Overlay the normal distribution curve
    ax.plot(
        bins,
        1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((bins - mu) ** 2) / (2 * sigma**2)),
        linewidth=2.5,
        color="#BF616A",
        label="Normal Curve",
    )

    # Highlight regions using different alpha values
    # These represent different confidence intervals
    ax.axvspan(-4, -0.67, color="#A3BE8C", alpha=0.1, label="Lower tail")
    ax.axvspan(-0.67, 0, color="#A3BE8C", alpha=0.2)
    ax.axvspan(0, 0.67, color="#A3BE8C", alpha=0.3)
    ax.axvspan(0.67, 4, color="#A3BE8C", alpha=0.4, label="Upper tail")

    # Add vertical lines for standard deviations
    ax.axvline(
        -0.67 * sigma + mu, color="#2E3440", linestyle="--", linewidth=1.5, alpha=0.5
    )
    ax.axvline(
        0.67 * sigma + mu, color="#2E3440", linestyle="--", linewidth=1.5, alpha=0.5
    )

    # Formatting
    remove_chartjunk(ax)
    ax.set_xlabel("Value (Standard Deviations)", fontsize=11)
    ax.set_ylabel("Probability Density", fontsize=11)
    ax.set_title(
        f"Normal Distribution (mu={mu}, sigma={sigma}) with Highlighted Regions",
        fontsize=13,
        pad=15,
    )
    ax.legend(frameon=False)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_normal_distribution.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_normal_distribution.png'}")

if __name__ == "__main__":
    main()
