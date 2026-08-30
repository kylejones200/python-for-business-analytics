"""Seasonal decomposition of monthly order volume."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = ops["order_date"].astype("datetime64[ns]")
ts = ops.set_index("order_date")["order_id"].resample("ME").count()
ts = ts.iloc[1:-1]
decomp = seasonal_decompose(ts, model="multiplicative", period=12)

print(f"n_months={len(ts)}")
print(f"trend_last={float(decomp.trend.dropna().iloc[-1]):.2f}")
print(f"seasonal_min={float(decomp.seasonal.min()):.3f}")
print(f"seasonal_max={float(decomp.seasonal.max()):.3f}")

fig = decomp.plot()
fig.set_size_inches(10, 7)
fig.tight_layout()
img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch10_seasonal_decomposition.png", dpi=300, bbox_inches="tight"
)
plt.close()
print("Saved img/ch10_seasonal_decomposition.png")
