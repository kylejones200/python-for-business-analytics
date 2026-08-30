"""Demonstrates missing data analysis and visualization.

This script shows how to identify, summarize, and visualize missing data
patterns in datasets. Readers learn missing data detection, summary statistics,
and visualization tools like missingno for understanding data completeness.

"""
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

try:
    import missingno as msno  # pip install missingno
    import matplotlib.pyplot as plt
except ImportError:
    msno = None
    plt = None

def main():
    """Main function demonstrating missing data analysis."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    from bookdata import load_frame

    # Load example dataset (local, reproducible)
    df = load_frame("business_ops")[
        [
            "order_date",
            "quantity",
            "unit_price_usd",
            "discount_rate",
            "net_value_usd",
            "satisfaction",
        ]
    ].copy()

    # Create artificial missingness for demonstration
    np.random.seed(42)
    df.loc[10:250, "satisfaction"] = np.nan
    df.loc[100:175, "discount_rate"] = np.nan

    # Basic missing value summary
    logger.info("Missing values per column:")
    logger.info(df.isnull().sum())
    logger.info(f"\nTotal missing: {df.isnull().sum().sum()}")
    logger.info(f"Percentage missing: {df.isnull().sum().sum() / df.size * 100:.1f}%")

    # Optional visualization (requires missingno)
    if msno is not None and plt is not None:
        msno.matrix(df.sample(500, random_state=42))
        script_path = Path(__file__)
        img_dir = script_path.parents[2] / "img"
        img_dir.mkdir(exist_ok=True)
        fig_filename = img_dir / f"{script_path.stem}.png"
        plt.savefig(fig_filename, dpi=150, bbox_inches="tight")
        logger.info(f"Missingness matrix saved to {fig_filename}")
        logger.info("\nNote: Install `missingno` + `matplotlib` to visualize missingness.")

if __name__ == "__main__":
    main()
