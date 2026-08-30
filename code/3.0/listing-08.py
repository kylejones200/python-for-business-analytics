"""

This script demonstrates creating box plots to compare distributions across
groups. Readers learn to visualize distributions, identify outliers, and
compare groups.
"""

import logging
import os
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import minimalist_style
from minimalist_style import set_minimalist_style
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


def main():
    """Create box plot comparing distributions across groups."""
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s: %(message)s'
    )
    # Load minimalist_style module
    minimalist_boxplot = minimalist_style.minimalist_boxplot

    # Set style
    set_minimalist_style()

    # Example: Website load times by server location
    np.random.seed(101)
    us_east = np.random.normal(120, 15, 100)
    us_west = np.random.normal(140, 20, 100)
    europe = np.random.normal(180, 25, 100)
    asia = np.random.normal(220, 30, 100)

    # Add some outliers
    us_east = np.append(us_east, [200, 210, 195])
    asia = np.append(asia, [350, 340])

    data = [us_east, us_west, europe, asia]
    labels = ["US East", "US West", "Europe", "Asia"]

    # Create box plot
    minimalist_boxplot(
        data,
        labels=labels,
        color="#5E81AC",
        ylabel="Load Time (milliseconds)",
        title="Website Performance by Server Location",
    )

    # Add reference line for target performance
    plt.axhline(
        150,
        color="#A3BE8C",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        label="Target (150ms)",
    )
    plt.legend(frameon=False)

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(
        img_dir / "ch3_performance_boxplot.png", dpi=150, bbox_inches="tight"
    )
    logger.info(f"Saved figure to {img_dir / 'ch3_performance_boxplot.png'}")

    # Log summary statistics
    logger.info("\nPerformance Summary:")
    for label, times in zip(labels, data):
        spread = np.abs(times - np.median(times))
        n_outliers = len(times[spread > 2 * np.std(times)])
        logger.info(
            f"{label:10s}: Median={np.median(times):.1f}ms, "
            f"IQR={np.percentile(times, 75)-np.percentile(times, 25):.1f}ms, "
            f"Outliers={n_outliers}"
        )


if __name__ == "__main__":
    main()
