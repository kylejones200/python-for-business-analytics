"""Apply Holt double exponential smoothing to daily net order value."""

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
    ops.set_index("order_date")["net_value_usd"]
    .resample("D")
    .sum()
    .asfreq("D")
    .fillna(0.0)
)

fit = ExponentialSmoothing(series, trend="add", seasonal=None).fit()
fitted = fit.fittedvalues
forecast = fit.forecast(14)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(
    series.index,
    series.values,
    color="0.55",
    linewidth=0.8,
    label="Daily net value",
)
ax.plot(
    fitted.index,
    fitted.values,
    color="0.10",
    linewidth=1.6,
    label="Holt fitted values",
)
ax.plot(
    forecast.index,
    forecast.values,
    color="0.10",
    linestyle="--",
    linewidth=1.6,
    label="14-day forecast",
)
ax.set_xlabel("Date")
ax.set_ylabel("Net value (USD)")
ax.set_title("Double exponential smoothing (Holt) of daily net order value")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch7_double_exponential_smoothing.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)
print("Saved img/ch7_double_exponential_smoothing.png")
print("Last fitted value:", round(float(fitted.iloc[-1]), 2))
print("14-day forecast mean:", round(float(forecast.mean()), 2))
