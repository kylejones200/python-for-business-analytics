"""Compare adoption gaps across regions with overlaid histograms.

This script demonstrates visual comparison for t-test setup.

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
    """Create adoption gap comparison by region."""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s"
    )

    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    from bookdata import ensure_dataset

    df = pd.read_parquet(ensure_dataset("business_customers"))
    df["adoption_gap"] = 1.0 - df["adoption"]

    # Compare Northeast vs South regions
    northeast = df[df["region"] == "Northeast"]["adoption_gap"]
    south = df[df["region"] == "South"]["adoption_gap"]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(
        northeast,
        bins=30,
        alpha=0.6,
        color="#5E81AC",
        label="Northeast",
        edgecolor="black",
    )
    ax.hist(
        south,
        bins=30,
        alpha=0.6,
        color="#A3BE8C",
        label="South",
        edgecolor="black",
    )

    ax.set_xlabel("Adoption Gap", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title(
        "Adoption Gap Distribution by Region", fontsize=14, fontweight="bold"
    )
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    output_path = ROOT / "img" / "ch4_adoption_gap_by_region.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")

    # Log statistics
    logger.info(f"Northeast: mean={northeast.mean():.4f}, n={len(northeast)}")
    logger.info(f"South: mean={south.mean():.4f}, n={len(south)}")

    plt.close()


if __name__ == "__main__":
    main()
