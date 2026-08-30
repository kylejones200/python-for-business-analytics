"""

This script demonstrates creating heatmaps with custom color scales and annotations.
Readers learn to visualize two-dimensional data matrices with value labels.
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
    """Create heatmap with custom styling and annotations."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module

    # Set style
    set_minimalist_style()

    # Example: Customer satisfaction by product and region
    products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
    regions = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]

    # Generate satisfaction scores (1-10)
    np.random.seed(303)
    satisfaction_matrix = np.random.uniform(6, 9, (5, 5))
    satisfaction_matrix[2, 3] = 4.5  # Add a problem area
    satisfaction_matrix[0, 4] = 9.5  # Add an excellent area

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(satisfaction_matrix, cmap="RdYlGn", aspect="auto", vmin=4, vmax=10)

    # Set ticks and labels
    ax.set_xticks(np.arange(len(regions)))
    ax.set_yticks(np.arange(len(products)))
    ax.set_xticklabels(regions)
    ax.set_yticklabels(products)

    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # Add values in cells
    for i in range(len(products)):
        for j in range(len(regions)):
            text = ax.text(
                j,
                i,
                f"{satisfaction_matrix[i, j]:.1f}",
                ha="center",
                va="center",
                color="#2E3440",
                fontsize=10,
                fontweight="bold",
            )

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Satisfaction Score", rotation=270, labelpad=20, fontsize=10)

    # Formatting
    ax.set_xlabel("Region", fontsize=11)
    ax.set_ylabel("Product", fontsize=11)
    ax.set_title(
        "Customer Satisfaction Heatmap by Product and Region", fontsize=13, pad=15
    )

    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xticks(np.arange(len(regions) + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(products) + 1) - 0.5, minor=True)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_satisfaction_heatmap.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_satisfaction_heatmap.png'}")

if __name__ == "__main__":
    main()
