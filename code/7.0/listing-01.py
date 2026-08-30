"""Fit an ARIMA(1,1,1) model to daily net order value."""

import sys
from pathlib import Path

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
ts = (
    ops.set_index("order_date")["net_value_usd"]
    .resample("D")
    .sum()
    .asfreq("D")
    .fillna(0.0)
)

model = ARIMA(ts, order=(1, 1, 1))
fit = model.fit()
forecast = fit.forecast(steps=10)

print("Daily observations:", len(ts))
print("Date range:", ts.index.min().date(), "to", ts.index.max().date())
print("ARIMA(1,1,1) 10-day forecast (USD):")
print(forecast.round(2).to_string())
