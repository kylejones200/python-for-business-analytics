"""Compare adoption gaps by onboarding status with overlaid histograms.

This script demonstrates comparison for non-significant difference.

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
    """Create adoption gap comparison by onboarding status."""
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

    # Compare by onboarding complete status
    onboarded = df[df["onboarding_complete"] == True]["adoption_gap"]
    not_onboarded = df[df["onboarding_complete"] == False]["adoption_gap"]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(
        onboarded,
        bins=30,
        alpha=0.6,
        color="#88C0D0",
        label="Onboarding Complete",
        edgecolor="black",
    )
    ax.hist(
        not_onboarded,
        bins=30,
        alpha=0.6,
        color="#D08770",
        label="Onboarding Incomplete",
        edgecolor="black",
    )

    ax.set_xlabel("Adoption Gap", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title(
        "Adoption Gap by Onboarding Status", fontsize=14, fontweight="bold"
    )
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    output_path = ROOT / "img" / "ch4_adoption_gap_by_onboarding.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")

    # Log statistics
    logger.info(f"Onboarded: mean={onboarded.mean():.4f}, n={len(onboarded)}")
    logger.info(
        f"Not Onboarded: mean={not_onboarded.mean():.4f}, "
        f"n={len(not_onboarded)}"
    )

    plt.close()


if __name__ == "__main__":
    main()
