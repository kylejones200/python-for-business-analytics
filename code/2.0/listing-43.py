"""Demonstrates missing data visualization using missingno library.

This script shows how to visualize missing data patterns using missingno's bar
charts, matrix plots, and heatmaps. Readers learn missing data visualization,
pattern identification, and data completeness analysis.

"""

import logging
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

try:
    import missingno as msno
except ImportError:
    msno = None
    logger.warning("missingno not installed; using matplotlib fallback.")


def main():
    """Main function demonstrating missing data visualization."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Load or create example data with missing values
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    try:
        from bookdata import ensure_dataset

        ops_path = ensure_dataset("business_ops")
        if ops_path:
            df = pd.read_parquet(ops_path)[
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
        else:
            # Create synthetic data with missing values
            np.random.seed(42)
            df = pd.DataFrame(
                {
                    'col1': np.random.normal(0, 1, 500),
                    'col2': np.random.normal(0, 1, 500),
                    'col3': np.random.normal(0, 1, 500),
                    'col4': np.random.normal(0, 1, 500),
                }
            )
            df.loc[10:250, "col1"] = np.nan
            df.loc[100:175, "col2"] = np.nan
    except ImportError:
        np.random.seed(42)
        df = pd.DataFrame(
            {
                'col1': np.random.normal(0, 1, 500),
                'col2': np.random.normal(0, 1, 500),
                'col3': np.random.normal(0, 1, 500),
                'col4': np.random.normal(0, 1, 500),
            }
        )
        df.loc[10:250, "col1"] = np.nan
        df.loc[100:175, "col2"] = np.nan

    script_path = Path(__file__)
    img_dir = script_path.parents[2] / "img"
    img_dir.mkdir(parents=True, exist_ok=True)

    # Bar chart showing missing values per column
    if msno is not None:
        msno.bar(df)
        plt.title("Missing Values per Column")
    else:
        missing_counts = df.isna().sum().sort_values(ascending=False)
        plt.figure(figsize=(8, 4))
        missing_counts.plot(kind="bar", color="steelblue", edgecolor="black")
        plt.title("Missing Values per Column")
        plt.ylabel("Missing count")
    plt.tight_layout()
    fig_filename1 = img_dir / f"{script_path.stem}_bar.png"
    plt.savefig(fig_filename1, dpi=150, bbox_inches="tight")
    logger.info(f"Bar chart saved to {fig_filename1}")
    # Matrix showing missing data pattern
    if msno is not None:
        msno.matrix(df)
        plt.title("Missingness Pattern Matrix")
    else:
        miss = df.isna().to_numpy(dtype=int)
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.imshow(miss, aspect="auto", interpolation="nearest", cmap="gray_r")
        ax.set_title("Missingness Pattern Matrix")
        ax.set_xlabel("Columns")
        ax.set_ylabel("Rows")
    plt.tight_layout()
    fig_filename2 = img_dir / f"{script_path.stem}_matrix.png"
    plt.savefig(fig_filename2, dpi=150, bbox_inches="tight")
    logger.info(f"Matrix plot saved to {fig_filename2}")
    # Heatmap showing correlation of missingness between columns
    if msno is not None:
        msno.heatmap(df)
        plt.title("Missingness Correlation Heatmap")
    else:
        corr = df.isna().corr()
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(corr.to_numpy(), cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")
        ax.set_yticks(range(len(corr.index)))
        ax.set_yticklabels(corr.index)
        ax.set_title("Missingness Correlation Heatmap")
        fig.colorbar(im, ax=ax, label="Correlation")
    plt.tight_layout()
    fig_filename3 = img_dir / f"{script_path.stem}_heatmap.png"
    plt.savefig(fig_filename3, dpi=150, bbox_inches="tight")
    logger.info(f"Heatmap saved to {fig_filename3}")


if __name__ == "__main__":
    main()
