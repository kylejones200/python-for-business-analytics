"""Create histogram of MRR distribution for statistical analysis.

This script demonstrates visualizing a continuous variable for hypothesis testing.

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
    """Create MRR histogram."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    
    from bookdata import ensure_dataset
    
    df = pd.read_parquet(ensure_dataset("business_customers"))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["mrr_usd"], bins=50, color="#5E81AC", alpha=0.7, edgecolor="black")
    ax.set_xlabel("Monthly Recurring Revenue (USD)", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Customer MRR", fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    
    # Add mean line
    mean_mrr = df["mrr_usd"].mean()
    ax.axvline(mean_mrr, color="red", linestyle="--", linewidth=2,
              label=f"Mean: ${mean_mrr:,.0f}")
    ax.legend()
    
    output_path = ROOT / "img" / "ch4_mrr_histogram.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
