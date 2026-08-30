"""Fit a SARIMA model to monthly net order value with yearly seasonality."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
weekly = (
    ops.set_index("order_date")["net_value_usd"]
    .resample("W")
    .sum()
    .asfreq("W")
    .fillna(0.0)
)

model = SARIMAX(
    weekly,
    order=(1, 1, 1),
    seasonal_order=(1, 0, 1, 4),
    enforce_stationarity=False,
    enforce_invertibility=False,
)
results = model.fit(disp=False)
forecast = results.forecast(steps=8)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(weekly.index, weekly.values, label="Weekly net value")
ax.plot(forecast.index, forecast.values, label="8-week forecast")
ax.set_title("SARIMA forecast of weekly net order value")
ax.set_ylabel("USD")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_sarima_forecast.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_sarima_forecast.png")
print(results.summary().tables[1])
print(forecast.round(2).to_string())
