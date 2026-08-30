"""

This script demonstrates creating multi-panel dashboards with multiple visualizations.
Readers learn to combine multiple plots into a cohesive dashboard layout.
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
import pandas as pd

logger = logging.getLogger(__name__)

def main():
    """Create multi-panel business performance dashboard."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Load minimalist_style module
    remove_chartjunk = minimalist_style.remove_chartjunk
    get_minimalist_colors = minimalist_style.get_minimalist_colors

    # Set style
    set_minimalist_style()
    colors = get_minimalist_colors(4)

    # Generate realistic business data
    np.random.seed(202)
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    revenue = np.array([120, 125, 135, 140, 155, 160, 158, 165, 170, 180, 195, 210])
    costs = np.array([85, 88, 92, 95, 98, 102, 100, 105, 108, 110, 115, 120])
    profit = revenue - costs

    customers = np.array(
        [1200, 1350, 1500, 1450, 1600, 1700, 1650, 1800, 1900, 2000, 2200, 2400]
    )

    satisfaction = np.array(
        [7.2, 7.4, 7.3, 7.5, 7.8, 7.7, 7.9, 7.8, 8.0, 8.1, 8.2, 8.3]
    )

    # Create 2x2 dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Q4 Business Performance Dashboard", fontsize=15, y=0.995)

    # Panel 1: Revenue and Costs
    ax1 = axes[0, 0]
    x = np.arange(len(months))
    width = 0.35
    ax1.bar(x - width / 2, revenue, width, color=colors[0], alpha=0.7, label="Revenue")
    ax1.bar(x + width / 2, costs, width, color=colors[1], alpha=0.7, label="Costs")
    remove_chartjunk(ax1)
    ax1.set_ylabel("Amount ($1000s)", fontsize=10)
    ax1.set_title("Revenue vs Costs", fontsize=12, pad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(months, rotation=45, ha="right", fontsize=8)
    ax1.legend(frameon=False, fontsize=9)

    # Panel 2: Profit Trend
    ax2 = axes[0, 1]
    ax2.plot(months, profit, color=colors[2], linewidth=2.5, marker="o", markersize=6)
    ax2.fill_between(range(len(months)), profit, alpha=0.2, color=colors[2])
    remove_chartjunk(ax2)
    ax2.set_ylabel("Profit ($1000s)", fontsize=10)
    ax2.set_title("Monthly Profit", fontsize=12, pad=10)
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    # Add growth annotation
    growth = ((profit[-1] - profit[0]) / profit[0]) * 100
    ax2.text(
        0.98,
        0.98,
        f"+{growth:.1f}% YTD",
        transform=ax2.transAxes,
        fontsize=11,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="#A3BE8C", alpha=0.3, edgecolor="none"),
    )

    # Panel 3: Customer Growth
    ax3 = axes[1, 0]
    ax3.plot(
        months, customers, color=colors[3], linewidth=2.5, marker="s", markersize=6
    )
    remove_chartjunk(ax3)
    ax3.set_ylabel("Total Customers", fontsize=10)
    ax3.set_title("Customer Base Growth", fontsize=12, pad=10)
    plt.setp(ax3.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    # Format y-axis with commas
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{int(x):,}"))

    # Panel 4: Satisfaction Score
    ax4 = axes[1, 1]
    ax4.plot(
        months, satisfaction, color="#5E81AC", linewidth=2.5, marker="o", markersize=6
    )
    ax4.axhline(
        8.0,
        color="#A3BE8C",
        linestyle="--",
        linewidth=1.5,
        alpha=0.5,
        label="Target (8.0)",
    )
    remove_chartjunk(ax4)
    ax4.set_ylabel("Satisfaction Score", fontsize=10)
    ax4.set_title("Customer Satisfaction", fontsize=12, pad=10)
    ax4.set_ylim(6.5, 8.5)
    plt.setp(ax4.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    ax4.legend(frameon=False, fontsize=9)

    plt.tight_layout()

    # Save figure before showing
    img_dir = Path(__file__).resolve().parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    plt.savefig(img_dir / "ch3_business_dashboard.png", dpi=150, bbox_inches="tight")
    logger.info(f"Saved figure to {img_dir / 'ch3_business_dashboard.png'}")

    # Log summary
    logger.info("\nKey Performance Indicators:")
    logger.info(
        f"  Total Revenue: ${revenue.sum()}K ({((revenue[-1]-revenue[0])/revenue[0]*100):+.1f}%)"
    )
    logger.info(
        f"  Total Profit:  ${profit.sum()}K ({((profit[-1]-profit[0])/profit[0]*100):+.1f}%)"
    )
    logger.info(
        f"  Customers:     {customers[-1]:,} ({((customers[-1]-customers[0])/customers[0]*100):+.1f}%)"
    )
    logger.info(
        f"  Satisfaction:  {satisfaction[-1]:.1f}/10 ({satisfaction[-1]-satisfaction[0]:+.1f} pts)"
    )

if __name__ == "__main__":
    main()
