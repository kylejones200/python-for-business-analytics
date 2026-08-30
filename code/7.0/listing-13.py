"""Forecast U.S. unemployment 12 months ahead with exponential smoothing."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("fred_series")
df["date"] = pd.to_datetime(df["date"])
series = (
    df.loc[df["UNRATE"].notna(), ["date", "UNRATE"]]
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
series.plot(ax=ax, label="Observed")
forecast.plot(ax=ax, label="Forecast")
ax.set_ylabel("Unemployment rate (%)")
ax.set_title("12-month unemployment forecast")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_exponential_smoothing_forecast.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_exponential_smoothing_forecast.png")
print(forecast.round(2).to_string())
