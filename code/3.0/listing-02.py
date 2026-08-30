"""

This script demonstrates the visual impact of minimalist styling through side-
by-side comparison. Readers learn to appreciate how styling choices affect
data visualization clarity and professionalism.
"""

import logging
import os
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from minimalist_style import set_minimalist_style, minimalist_histogram
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def main():
    """Create side-by-side comparison of default vs minimalist styling."""
    logging.basicConfig(
        level=logging.INFO, format='%(levelname)s: %(message)s'
    )
    # Generate sample data: customer satisfaction scores
    np.random.seed(42)
    satisfaction = np.random.normal(7.5, 1.5, 500)
    satisfaction = np.clip(satisfaction, 1, 10)  # Constrain to 1-10 scale

    # Create side-by-side comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # LEFT: Default matplotlib style
    ax1.hist(
        satisfaction, bins=20, color="blue", edgecolor="black", alpha=0.7
    )
    ax1.set_xlabel("Satisfaction Score")
    ax1.set_ylabel("Number of Customers")
    ax1.set_title("Default Matplotlib Style")

    # RIGHT: Minimalist style
    set_minimalist_style()
    minimalist_histogram(
        satisfaction,
        ax=ax2,
        bins=20,
        color="#5E81AC",
        xlabel="Satisfaction Score",
        ylabel="Number of Customers",
        title="Minimalist Style",
    )

    plt.suptitle("The Impact of Minimalist Styling", fontsize=14, y=1.02)
    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(
        img_dir / "ch3_style_comparison.png", dpi=150, bbox_inches="tight"
    )
    logger.info(f"Saved figure to {img_dir / 'ch3_style_comparison.png'}")


if __name__ == "__main__":
    main()
