"""Decompose daily order volume into trend, weekly seasonality, and residual."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
series = (
    ops.set_index("order_date")["order_id"]
    .resample("D")
    .count()
    .asfreq("D")
    .fillna(0)
)

decomp = seasonal_decompose(series, model="additive", period=7)
fig = decomp.plot()
fig.set_size_inches(10, 8)
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_model_components.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_model_components.png")
print("Trend at last available date:", round(float(decomp.trend.dropna().iloc[-1]), 2))
print("Seasonal range:", round(float(decomp.seasonal.min()), 2), "to", round(float(decomp.seasonal.max()), 2))
