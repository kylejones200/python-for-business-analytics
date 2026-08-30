"""Create daily sales time series plot.

This script demonstrates basic time series visualization using business operations data.

"""
import logging
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Create daily sales time series."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    
    from bookdata import ensure_dataset
    
    ops_path = ensure_dataset("business_ops")
    if ops_path is None:
        raise FileNotFoundError("business_ops dataset unavailable")
    
    df = pd.read_parquet(ops_path)
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    # Create daily sales time series
    daily_sales = df.groupby("order_date")["net_value_usd"].sum().sort_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_sales.index, daily_sales.values, color="#5E81AC", linewidth=1.5)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Daily Sales (USD)", fontsize=12)
    ax.set_title("Daily Net Sales Over Time", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    output_path = ROOT / "img" / "ch7_daily_net_order_value.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")
    
    if os.environ.get("CODE_RUN_ALL") == "1":
        plt.close()
    
    logger.info(f"Daily sales range: ${daily_sales.min():,.0f} to ${daily_sales.max():,.0f}")
    logger.info(f"Average daily sales: ${daily_sales.mean():,.0f}")


if __name__ == "__main__":
    main()
