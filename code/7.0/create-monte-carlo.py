"""Create Monte Carlo simulation for sales forecasting.

"""
import logging
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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
    
    # Calculate returns (percent changes)
    returns = daily_sales.pct_change().dropna()
    mu = returns.mean()
    sigma = returns.std()
    
    # Monte Carlo simulation
    np.random.seed(42)
    num_simulations = 100
    num_days = 90
    last_price = daily_sales.iloc[-1]
    
    # Generate simulation paths
    simulations = np.zeros((num_days, num_simulations))
    simulations[0] = last_price
    
    for t in range(1, num_days):
        shock = np.random.normal(mu, sigma, num_simulations)
        simulations[t] = simulations[t-1] * (1 + shock)
    
    # Plot paths
    fig, ax = plt.subplots(figsize=(12, 6))
    for i in range(num_simulations):
        ax.plot(simulations[:, i], color="#5E81AC", alpha=0.1, linewidth=0.5)
    
    # Add mean path
    mean_path = simulations.mean(axis=1)
    ax.plot(mean_path, color="#BF616A", linewidth=2.5, label="Mean Path")
    
    ax.set_xlabel("Days Ahead", fontsize=12)
    ax.set_ylabel("Forecasted Daily Sales (USD)", fontsize=12)
    ax.set_title("Monte Carlo Simulation: 90-Day Sales Forecast", 
                fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    output_path = ROOT / "img" / "ch7_monte_carlo_paths.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")
    plt.close()
    
    # Histogram of final values
    final_values = simulations[-1]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(final_values, bins=30, color="#A3BE8C", alpha=0.7, edgecolor="black")
    ax.axvline(final_values.mean(), color="red", linestyle="--", 
              linewidth=2, label=f"Mean: ${final_values.mean():,.0f}")
    ax.set_xlabel("Final Daily Sales (USD)", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of 90-Day Ahead Sales Forecasts", 
                fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    output_path = ROOT / "img" / "ch7_monte_carlo_histogram.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    logger.info(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
