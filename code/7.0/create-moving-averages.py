"""Create moving average plots for daily sales.

This script demonstrates smoothing techniques with moving averages.

"""
import logging
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


def main():
    """Create moving average plots."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    ROOT = Path(__file__).resolve().parents[2]
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    
    from bookdata import ensure_dataset
    
    df = pd.read_parquet(ensure_dataset("business_ops"))
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    # Create daily sales time series
    daily_sales = df.groupby("order_date")["net_value_usd"].sum().sort_index()
    
    # Create 5-day, 30-day, and 90-day moving averages
    windows = [5, 30, 90]
    
    for window in windows:
        ma = daily_sales.rolling(window=window).mean()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_sales.index, daily_sales.values, color="#5E81AC", 
               alpha=0.6, linewidth=1, label="Daily Sales")
        ax.plot(ma.index, ma.values, color="#A3BE8C", 
               linewidth=2.5, label=f"{window}-Day Moving Average")
        
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Daily Sales (USD)", fontsize=12)
        ax.set_title(f"Daily Sales with {window}-Day Moving Average", 
                    fontsize=14, fontweight="bold")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        output_path = ROOT / "img" / f"ch7_moving_avg_{window}day.png"
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        logger.info(f"Saved: {output_path}")
        plt.close()


if __name__ == "__main__":
    main()
