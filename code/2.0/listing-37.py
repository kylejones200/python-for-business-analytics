"""Demonstrates plotting normal distributions with histogram overlays.

This script shows how to create histograms of normally distributed data and
overlay the theoretical probability density function. Readers learn
statistical visualization, histogram creation, and comparing empirical
distributions to theoretical models.

"""

import logging
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


def plot_norm_hist(s, mu, sigma, vline=True, title=True):
    """Plot histogram of data with theoretical normal distribution overlay.

    Args:
        s: Array of sample data.
        mu: Mean of the distribution.
        sigma: Standard deviation of the distribution.
        vline: Whether to add vertical lines at +/-0.67 sigma.
        title: Whether to add a title to the plot.
    """
    count, bins, ignored = plt.hist(s, 30, density=True)
    plt.plot(
        bins,
        1
        / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-((bins - mu) ** 2) / (2 * sigma**2)),
        linewidth=2,
        color="r",
    )

    if vline:
        lline = -0.67 * sigma + mu
        uline = 0.67 * sigma + mu
        plt.axvline(lline, color="g")
        plt.axvline(uline, color="g")

    if title:
        plt.title(
            "Normal distribution with mean: {:.02f} "
            "and StDev: {:.02f}".format(mu, sigma)
        )


def main():
    """Main function demonstrating normal distribution visualization."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Set random seed for reproducibility
    np.random.seed(42)

    mu, sigma = 0, 1  # mean and standard deviation
    s = np.random.normal(mu, sigma, 1000)

    plot_norm_hist(s, mu, sigma, vline=True, title=True)

    # Save figure before showing
    script_path = Path(__file__)
    img_dir = script_path.parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    fig_filename = img_dir / "ch2_normal_1000.png"
    plt.savefig(fig_filename, dpi=300, bbox_inches="tight")
    logger.info(f"Figure saved to {fig_filename}")
    plt.close()


if __name__ == "__main__":
    main()
