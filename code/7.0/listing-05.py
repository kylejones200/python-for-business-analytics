"""Plot 5-, 30-, and 90-day moving averages of daily net order value."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
series = ops.set_index("order_date")["net_value_usd"].resample("D").sum().asfreq("D").fillna(0.0)

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)

for window in (5, 30, 90):
    ma = series.rolling(window=window, min_periods=1).mean()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(series.index, series.values, color="0.55", linewidth=0.8, label="Daily net value")
    ax.plot(ma.index, ma.values, color="0.15", linewidth=2.0, label=f"{window}-day moving average")
    ax.set_xlabel("Date")
    ax.set_ylabel("Net value (USD)")
    ax.set_title(f"Daily net order value with a {window}-day moving average")
    ax.legend()
    fig.tight_layout()
    out = img_dir / f"ch7_moving_avg_{window}day.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved", out.relative_to(ROOT))
    print(f"{window}-day MA last value: {ma.iloc[-1]:.2f}")
