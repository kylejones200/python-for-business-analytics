"""Forecast the next 90 days of daily order volume."""

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
    .asfreq("D")
    .fillna(0)
)

fit = ExponentialSmoothing(series, trend="add", seasonal="add", seasonal_periods=7).fit()
forecast = fit.forecast(90)

fig, ax = plt.subplots(figsize=(10, 4))
series.plot(ax=ax, label="Observed")
forecast.plot(ax=ax, label="90-day forecast")
ax.set_ylabel("Daily orders")
ax.set_title("90-day forecast of daily order volume")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_order_volume_forecast.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_order_volume_forecast.png")
print("90-day forecast total orders:", round(float(forecast.sum()), 1))
print(forecast.head().round(2).to_string())
