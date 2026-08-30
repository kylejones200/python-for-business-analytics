"""Create clean sales time series plot for initial visualization.

"""
import logging
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    
    from bookdata import ensure_dataset
    
    df = pd.read_parquet(ensure_dataset("business_ops"))
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    daily_sales = df.groupby("order_date")["net_value_usd"].sum().sort_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_sales.index, daily_sales.values, color="#5E81AC", linewidth=1.5)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Daily Sales (USD)", fontsize=12)
    ax.set_title("Daily Net Sales Time Series", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    output_path = ROOT / "img" / "ch7_sales_history.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
