"""Twelve-month moving average of monthly order volume."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = ops["order_date"].astype("datetime64[ns]")
ts = (
    ops.set_index("order_date")["order_id"]
    .resample("ME")
    .count()
    .to_frame("orders")
)
ts = ts.iloc[1:-1]
ts["ma_12"] = ts["orders"].rolling(window=12, min_periods=12).mean()

print(f"n_months={len(ts)}")
print(f"last_orders={float(ts['orders'].iloc[-1]):.1f}")
print(f"last_ma12={float(ts['ma_12'].dropna().iloc[-1]):.2f}")

plt.figure(figsize=(10, 5))
plt.plot(ts.index, ts["orders"], label="Monthly orders")
plt.plot(ts.index, ts["ma_12"], label="12-month moving average")
plt.xlabel("Month")
plt.ylabel("Orders")
plt.legend()
plt.tight_layout()
img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch10_moving_average.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch10_moving_average.png")
