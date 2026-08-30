"""

This script demonstrates creating horizontal bar charts with conditional coloring and reference lines.
Readers learn to visualize categorical comparisons and highlight values relative to targets.
"""
import logging
import os
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from minimalist_style import set_minimalist_style, remove_chartjunk
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def main():
    """Create horizontal bar chart with conditional coloring."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Example: Employee satisfaction by department
    departments = [
        "Customer Service",
        "Product Development",
        "Marketing & Sales",
        "Operations & Logistics",
        "Human Resources",
        "Finance & Accounting",
    ]
    satisfaction = [7.2, 8.1, 7.8, 6.9, 7.5, 7.4]

    # Create horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Color bars by value (red for low, green for high)
    colors = [
        "#BF616A" if s < 7.0 else "#A3BE8C" if s > 7.7 else "#5E81AC"
        for s in satisfaction
    ]

    bars = ax.barh(
        departments,
        satisfaction,
        color=colors,
        alpha=0.7,
        edgecolor="white",
        linewidth=1,
    )

    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, satisfaction)):
        ax.text(
            value + 0.1,
            i,
            f"{value:.1f}",
            va="center",
            ha="left",
            fontsize=10,
            color="#2E3440",
        )

    # Add reference line at target (7.5)
    ax.axvline(
        7.5,
        color="#4C566A",
        linestyle="--",
        linewidth=1.5,
        alpha=0.5,
        label="Target (7.5)",
    )

    # Formatting
    remove_chartjunk(ax)
    ax.set_xlabel("Satisfaction Score (1-10)", fontsize=11)
    ax.set_title("Employee Satisfaction by Department", fontsize=13, pad=15)
    ax.set_xlim(6, 9)
    ax.legend(frameon=False)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_satisfaction_bar.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_satisfaction_bar.png'}")

if __name__ == "__main__":
    main()
