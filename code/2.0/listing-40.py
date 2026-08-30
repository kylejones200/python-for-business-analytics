"""Demonstrates creating boxplots using matplotlib for distribution visualization.

This script shows how to create boxplots to visualize data distributions and
identify outliers. Readers learn boxplot creation, distribution visualization,
and statistical plot customization.

"""
import logging
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating boxplot creation."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    # Create example data (normally distributed)
    np.random.seed(42)
    s = np.random.normal(0, 1, 1000)
    
    fig1, ax1 = plt.subplots()
    ax1.set_title("Basic Plot")
    ax1.boxplot(s, showfliers=False, vert=False)
    
    # Save figure before showing
    script_path = Path(__file__)
    img_dir = script_path.parents[2] / "img"
    img_dir.mkdir(exist_ok=True)
    fig_filename = img_dir / "ch2_boxplot.png"
    plt.savefig(fig_filename, dpi=300, bbox_inches="tight")
    logger.info(f"Boxplot saved to {fig_filename}")
    plt.close()
if __name__ == "__main__":
    main()
