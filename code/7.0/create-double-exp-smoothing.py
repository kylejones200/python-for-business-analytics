"""Create double exponential smoothing plot.

"""
import logging
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

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
    
    # Fit double exponential smoothing (Holt's method - trend only)
    model = ExponentialSmoothing(daily_sales, trend="add", seasonal=None)
    fit = model.fit()
    forecast = fit.fittedvalues
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_sales.index, daily_sales.values, color="#5E81AC",
           alpha=0.6, linewidth=1, label="Actual Sales")
    ax.plot(forecast.index, forecast.values, color="#BF616A",
           linewidth=2, label="Double Exponential Smoothing")
    
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Daily Sales (USD)", fontsize=12)
    ax.set_title("Double Exponential Smoothing (Holt's Method)", 
                fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    output_path = ROOT / "img" / "ch7_double_exponential_smoothing.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
