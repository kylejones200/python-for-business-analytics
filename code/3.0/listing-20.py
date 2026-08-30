"""

This script demonstrates the importance of proper axis scaling in visualizations.
Readers learn how axis truncation can mislead viewers and when to use full vs truncated axes.
"""
import logging
import os
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import minimalist_style
from minimalist_style import set_minimalist_style
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def main():
    """Demonstrate proper vs misleading axis scaling."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    set_minimalist_style()

    # Example: Small difference in sales
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    sales = [98, 101, 99, 103]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # WRONG: Truncated axis
    ax1.bar(quarters, sales, color="#5E81AC", alpha=0.7)
    ax1.set_ylim(95, 105)  # Starts at 95, not 0
    remove_chartjunk(ax1)
    ax1.set_ylabel("Sales ($M)", fontsize=11)
    ax1.set_title("MISLEADING: Truncated Y-Axis", fontsize=12, color="#BF616A")

    # RIGHT: Full axis
    ax2.bar(quarters, sales, color="#5E81AC", alpha=0.7)
    ax2.set_ylim(0, 120)  # Starts at 0
    remove_chartjunk(ax2)
    ax2.set_ylabel("Sales ($M)", fontsize=11)
    ax2.set_title("HONEST: Full Y-Axis", fontsize=12, color="#A3BE8C")

    plt.suptitle("The Impact of Y-Axis Scaling", fontsize=14, y=1.02)
    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_axis_scaling.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_axis_scaling.png'}")

if __name__ == "__main__":
    main()
