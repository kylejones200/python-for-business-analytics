"""Compute and plot 20-day Bollinger Bands on daily net order value."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
df = (
    ops.set_index("order_date")["net_value_usd"]
    .resample("D")
    .sum()
    .asfreq("D")
    .ffill()
    .to_frame(name="net_value_usd")
)

df["20 Day MA"] = df["net_value_usd"].rolling(window=20, min_periods=1).mean()
rolling_std = df["net_value_usd"].rolling(window=20, min_periods=1).std()
df["20 Day MA_lower bound"] = df["20 Day MA"] - 2.0 * rolling_std
df["20 Day MA_upper bound"] = df["20 Day MA"] + 2.0 * rolling_std

fig, ax = plt.subplots(figsize=(10, 4))
ax.fill_between(
    df.index, df["20 Day MA_lower bound"], df["20 Day MA_upper bound"], alpha=0.25, color="0.70"
)
ax.plot(df.index, df["net_value_usd"], color="0.20", linewidth=1.0, label="Daily net value")
ax.plot(df.index, df["20 Day MA"], color="0.05", linewidth=1.4, label="20-day moving average")
ax.set_title("Bollinger Bands for daily net order value")
ax.set_xlabel("Date")
ax.set_ylabel("Net value (USD)")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_bollinger_bands.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_bollinger_bands.png")
print("Last 20-day MA:", round(float(df["20 Day MA"].iloc[-1]), 2))
print("Last upper/lower:", round(float(df["20 Day MA_upper bound"].iloc[-1]), 2),
      round(float(df["20 Day MA_lower bound"].iloc[-1]), 2))
