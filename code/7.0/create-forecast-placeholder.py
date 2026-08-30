"""Create simple ARIMA forecast visualization.

"""
import logging
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

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
    
    # Fit ARIMA model
    model = ARIMA(daily_sales, order=(1, 1, 1))
    fit = model.fit()
    
    # Forecast 30 days ahead
    forecast = fit.forecast(steps=30)
    forecast_index = pd.date_range(start=daily_sales.index[-1] + pd.Timedelta(days=1),
                                   periods=30, freq='D')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot historical data (last 180 days)
    ax.plot(daily_sales.index[-180:], daily_sales.values[-180:], 
           color="#5E81AC", linewidth=1.5, label="Historical Sales")
    
    # Plot forecast
    ax.plot(forecast_index, forecast, color="#BF616A", 
           linewidth=2, linestyle="--", label="ARIMA Forecast")
    
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Daily Sales (USD)", fontsize=12)
    ax.set_title("Daily Sales Forecast Using ARIMA(1,1,1)", 
                fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    output_path = ROOT / "img" / "ch7_arima_sales_forecast.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
