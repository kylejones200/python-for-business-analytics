"""Create histogram of adoption score differences for comparison analysis.

This script demonstrates creating a derived metric for statistical testing.

Chapter: Reasoning with Data and Uncertainty
Source: 4.0.tex
"""
import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Create adoption score histogram."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    
    from bookdata import ensure_dataset
    
    df = pd.read_parquet(ensure_dataset("business_customers"))
    
    # Create "adoption gap" metric (difference from maximum)
    df["adoption_gap"] = 1.0 - df["adoption"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["adoption_gap"], bins=40, color="#BF616A", alpha=0.7, edgecolor="black")
    ax.set_xlabel("Adoption Gap (1 - Adoption Score)", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Customer Adoption Gaps", fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    
    mean_gap = df["adoption_gap"].mean()
    ax.axvline(mean_gap, color="darkred", linestyle="--", linewidth=2,
              label=f"Mean Gap: {mean_gap:.3f}")
    ax.legend()
    
    output_path = ROOT / "img" / "ch4_adoption_gap_histogram.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
