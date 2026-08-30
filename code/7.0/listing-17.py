"""Forecast daily order volume with a weekly seasonal Holt-Winters model."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
series = (
    ops.set_index("order_date")["order_id"]
    .resample("D")
    .count()
    .rename("daily_orders")
    .asfreq("D")
    .fillna(0)
)

fit = ExponentialSmoothing(
    series, trend="add", seasonal="add", seasonal_periods=7
).fit()
forecast = fit.forecast(30)

fig, ax = plt.subplots(figsize=(10, 4))
series.plot(ax=ax, label="Observed daily orders")
forecast.plot(ax=ax, label="30-day forecast")
ax.set_ylabel("Orders")
ax.set_title("Daily order volume with a weekly seasonal forecast")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch7_seasonal_exponential_smoothing.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)
print("Saved img/ch7_seasonal_exponential_smoothing.png")
print("Mean daily orders:", round(float(series.mean()), 2))
print("Forecast mean:", round(float(forecast.mean()), 2))
