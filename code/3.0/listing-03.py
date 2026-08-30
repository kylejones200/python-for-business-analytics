"""

This script demonstrates creating a histogram with statistical overlays.
Readers learn to visualize distributions and highlight key statistics (mean,
median).
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
    """Create histogram with statistical overlays."""
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s: %(message)s'
    )
    # Load minimalist_style module
    minimalist_histogram = minimalist_style.minimalist_histogram

    # Set style
    set_minimalist_style()

    # Example: Transaction amounts
    np.random.seed(123)
    # Most transactions are low, few are very high (right-skewed)
    transactions = np.concatenate(
        [
            np.random.gamma(2, 20, 900),  # Regular transactions
            np.random.uniform(200, 500, 100),  # Some high-value transactions
        ]
    )

    # Create histogram
    minimalist_histogram(
        transactions,
        bins=30,
        color="#5E81AC",
        xlabel="Transaction Amount ($)",
        ylabel="Number of Transactions",
        title="Distribution of Transaction Amounts",
    )

    # Add statistics
    mean_val = np.mean(transactions)
    median_val = np.median(transactions)
    plt.axvline(
        mean_val,
        color="#BF616A",
        linestyle="--",
        linewidth=2,
        label=f"Mean: ${mean_val:.2f}",
    )
    plt.axvline(
        median_val,
        color="#A3BE8C",
        linestyle="--",
        linewidth=2,
        label=f"Median: ${median_val:.2f}",
    )
    plt.legend(frameon=False)

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(
        img_dir / "ch3_transaction_histogram.png",
        dpi=150,
        bbox_inches="tight",
    )
    logger.info(
        f"Saved figure to {img_dir / 'ch3_transaction_histogram.png'}"
    )

    # Log summary
    logger.info("Transaction Statistics:")
    logger.info(f"  Mean:   ${mean_val:.2f}")
    logger.info(f"  Median: ${median_val:.2f}")
    logger.info(f"  Std Dev: ${np.std(transactions):.2f}")
    logger.info(f"  Min:    ${np.min(transactions):.2f}")
    logger.info(f"  Max:    ${np.max(transactions):.2f}")


if __name__ == "__main__":
    main()
