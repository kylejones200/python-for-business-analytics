"""Demonstrates normal distribution visualization with large sample sizes.

This script shows how sample statistics converge to population parameters as
sample size increases. Readers learn statistical convergence, sample mean and
standard deviation calculations, and visualization of normal distributions.

"""
import logging
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating normal distribution with large samples."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    mu, sigma = 50, 10  # mean and standard deviation
    n = 100000
    s = np.random.normal(mu, sigma, n)

    mean_diff = abs(mu - np.mean(s))
    std_diff = abs(sigma - np.std(s, ddof=1))
    logger.info(f"Mean difference: {mean_diff:.4f}")
    logger.info(f"Std difference: {std_diff:.4f}")

    count, bins, ignored = plt.hist(s, 30, density=True, alpha=0.3)
    plt.plot(
        bins,
        1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((bins - mu) ** 2) / (2 * sigma**2)),
        linewidth=2,
        color="r",
    )
    lline = -0.67 * sigma + mu
    uline = 0.67 * sigma + mu
    plt.axvline(lline, color="g")
    plt.axvline(uline, color="g")
    plt.title(
        "Normal distribution with mean: {:.02f} and StDev: {:.02f}".format(mu, sigma)
    )
    
    # Save figure before showing
    script_path = Path(__file__)
    img_dir = script_path.parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    fig_filename = img_dir / "ch2_normal_100000.png"
    plt.savefig(fig_filename, dpi=300, bbox_inches="tight")
    logger.info(f"Figure saved to {fig_filename}")
    plt.close()
if __name__ == "__main__":
    main()
