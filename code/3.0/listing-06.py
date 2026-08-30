"""

This script demonstrates creating bar charts with value labels and conditional coloring.
Readers learn to visualize categorical data and highlight important categories.
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
    """Create bar chart with value labels and conditional coloring."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk

    # Set style
    set_minimalist_style()

    # Example: Sales by product category
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
    sales = [520, 380, 420, 290, 210, 180]

    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Color the highest bar differently
    colors = ["#5E81AC" if s != max(sales) else "#A3BE8C" for s in sales]

    bars = ax.bar(
        categories, sales, color=colors, alpha=0.7, edgecolor="white", linewidth=1
    )

    # Add value labels on bars
    for bar, value in zip(bars, sales):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 5,
            f"${value}K",
            ha="center",
            va="bottom",
            fontsize=10,
            color="#2E3440",
            fontweight="bold",
        )

    # Formatting
    remove_chartjunk(ax)
    ax.set_ylabel("Sales ($1000s)", fontsize=11)
    ax.set_title("Q4 Sales by Product Category", fontsize=13, pad=15)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_sales_by_category.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_sales_by_category.png'}")

    # Log insights
    total = sum(sales)
    logger.info(f"\nTotal Sales: ${total}K")
    logger.info(
        f"\nTop Category: {categories[sales.index(max(sales))]} (${max(sales)}K, {max(sales)/total*100:.1f}%)"
    )
    logger.info(
        f"Bottom Category: {categories[sales.index(min(sales))]} (${min(sales)}K, {min(sales)/total*100:.1f}%)"
    )

if __name__ == "__main__":
    main()
