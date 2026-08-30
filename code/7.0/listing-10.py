"""Load the cached FRED unemployment rate and plot a 12-month forecast."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

fred = load_frame("fred_series")
fred["date"] = pd.to_datetime(fred["date"])
series = (
    fred.loc[fred["UNRATE"].notna(), ["date", "UNRATE"]]
    .set_index("date")["UNRATE"]
    .sort_index()
    .resample("MS")
    .mean()
    .interpolate(limit=2)
    .dropna()
)

fit = ExponentialSmoothing(series, trend="add", seasonal=None).fit()
forecast = fit.forecast(12)

fig, ax = plt.subplots(figsize=(10, 4))
series.plot(ax=ax, label="Observed UNRATE")
forecast.plot(ax=ax, label="12-month forecast")
ax.set_ylabel("Unemployment rate (%)")
ax.set_title("U.S. unemployment rate with an exponential-smoothing forecast")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch7_unemployment_forecast.png", dpi=300, bbox_inches="tight"
)
plt.close(fig)
print("Saved img/ch7_unemployment_forecast.png")
print(series.tail(3).to_string())
print("Forecast:")
print(forecast.round(2).to_string())
