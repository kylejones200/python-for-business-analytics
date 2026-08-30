"""Forecast monthly order volume with ARIMA."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = ops["order_date"].astype("datetime64[ns]")
ts = ops.set_index("order_date")["order_id"].resample("ME").count()
ts = ts.iloc[1:-1]
model = ARIMA(ts, order=(1, 1, 1)).fit()
forecast = model.forecast(steps=12)

print(f"n_months={len(ts)}")
print(f"last_observed={float(ts.iloc[-1]):.1f}")
print(f"forecast_mean={float(forecast.mean()):.2f}")
print(f"forecast_min={float(forecast.min()):.2f}")
print(f"forecast_max={float(forecast.max()):.2f}")

plt.figure(figsize=(10, 5))
plt.plot(ts.index, ts, label="Observed monthly orders")
plt.plot(forecast.index, forecast, label="ARIMA(1,1,1) forecast")
plt.xlabel("Month")
plt.ylabel("Orders")
plt.legend()
plt.tight_layout()
img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(
    img_dir / "ch10_monthly_order_forecast.png", dpi=300, bbox_inches="tight"
)
plt.close()
print("Saved img/ch10_monthly_order_forecast.png")
