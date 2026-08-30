"""Compare simple exponential smoothing at two smoothing weights."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame


def exponential_smoothing(values, alpha):
    """One-parameter exponential smoothing of a 1-D series."""
    smoothed = np.empty_like(values, dtype=float)
    smoothed[0] = values[0]
    for i in range(1, len(values)):
        smoothed[i] = alpha * values[i] + (1.0 - alpha) * smoothed[i - 1]
    return smoothed


ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
series = (
    ops.set_index("order_date")["net_value_usd"]
    .resample("D")
    .sum()
    .asfreq("D")
    .fillna(0.0)
)
values = series.to_numpy(dtype=float)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(
    series.index, values, color="0.65", linewidth=0.8, label="Daily net value"
)
for alpha in (0.05, 0.30):
    sm = exponential_smoothing(values, alpha)
    ax.plot(series.index, sm, linewidth=1.8, label=f"alpha = {alpha:.2f}")
    print(f"alpha={alpha:.2f} last smoothed value: {sm[-1]:.2f}")
ax.set_xlabel("Date")
ax.set_ylabel("Net value (USD)")
ax.set_title("Simple exponential smoothing of daily net order value")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch7_exponential_smoothing.png", dpi=300, bbox_inches="tight"
)
plt.close(fig)
print("Saved img/ch7_exponential_smoothing.png")
