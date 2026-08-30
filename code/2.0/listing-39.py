"""Demonstrates normal distribution visualization with probability regions.

This script shows how to visualize probability regions of a normal
distribution using axvspan. Readers learn probability regions, standard
deviation intervals, and advanced matplotlib visualization techniques.

"""

import logging
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating probability region visualization."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Set random seed for reproducibility
    np.random.seed(42)

    mu, sigma = 0, 1  # mean and standard deviation
    s = np.random.normal(mu, sigma, 1000)

    mean_diff = abs(mu - np.mean(s))
    std_diff = abs(sigma - np.std(s, ddof=1))
    logger.info(f"Mean difference: {mean_diff:.4f}")
    logger.info(f"Std difference: {std_diff:.4f}")

    count, bins, ignored = plt.hist(s, 30, density=True, alpha=0.5)
    plt.plot(
        bins,
        1
        / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-((bins - mu) ** 2) / (2 * sigma**2)),
        linewidth=2,
        color="r",
    )
    plt.axvspan(-4, -0.67, color="g", alpha=0.1)
    plt.axvspan(-0.67, 0, color="g", alpha=0.2)
    plt.axvspan(0, 0.67, color="g", alpha=0.3)
    plt.axvspan(0.67, 4, color="g", alpha=0.4)

    # Save figure before showing
    script_path = Path(__file__)
    img_dir = script_path.parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    fig_filename = img_dir / "ch2_colored_normal.png"
    plt.savefig(fig_filename, dpi=300, bbox_inches="tight")
    logger.info(f"Figure saved to {fig_filename}")
    plt.close()


if __name__ == "__main__":
    main()
