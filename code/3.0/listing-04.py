"""

This script demonstrates creating scatter plots with trend lines and outlier highlighting.
Readers learn to visualize relationships between variables and identify outliers.
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
    """Create scatter plot with trend line and outlier highlighting."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module
    minimalist_scatter = minimalist_style.minimalist_scatter

    # Set style
    set_minimalist_style()

    # Example: Marketing spend vs Revenue
    np.random.seed(456)
    marketing = np.random.uniform(10, 150, 100)
    # Revenue correlates with marketing, with some noise
    revenue = marketing * 2.8 + np.random.normal(0, 30, 100)
    # Add a few outliers
    outlier_indices = [5, 23, 67]
    revenue[outlier_indices] += np.random.uniform(150, 250, len(outlier_indices))

    # Create scatter plot with highlighted outliers
    minimalist_scatter(
        marketing,
        revenue,
        size=60,
        alpha=0.6,
        color="#5E81AC",
        highlight_points=outlier_indices,
        xlabel="Marketing Spend ($1000s)",
        ylabel="Revenue ($1000s)",
        title="Marketing ROI: Spend vs Revenue",
    )

    # Add trend line
    z = np.polyfit(marketing, revenue, 1)
    p = np.poly1d(z)
    x_line = np.linspace(marketing.min(), marketing.max(), 100)
    plt.plot(
        x_line,
        p(x_line),
        color="#4C566A",
        linestyle="--",
        linewidth=1.5,
        alpha=0.5,
        label="Trend Line",
    )
    plt.legend(frameon=False)

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_marketing_roi.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_marketing_roi.png'}")

    # Calculate correlation
    correlation = np.corrcoef(marketing, revenue)[0, 1]
    logger.info(f"Correlation coefficient: {correlation:.3f}")

if __name__ == "__main__":
    main()
