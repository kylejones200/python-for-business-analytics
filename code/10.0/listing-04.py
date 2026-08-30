"""Year-by-month heatmap of order volume."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = ops["order_date"].astype("datetime64[ns]")
monthly = (
    ops.set_index("order_date")["order_id"]
    .resample("ME")
    .count()
    .rename("orders")
    .to_frame()
)
monthly = monthly.iloc[1:-1]
monthly["year"] = monthly.index.year
monthly["month"] = monthly.index.month
heatmap = monthly.pivot_table(index="month", columns="year", values="orders")

print(f"years={list(heatmap.columns)}")
print(f"peak_cell={float(heatmap.max().max()):.1f}")
print(f"trough_cell={float(heatmap.min().min()):.1f}")

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap, cmap="YlOrRd")
plt.xlabel("Year")
plt.ylabel("Month")
plt.tight_layout()
img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch10_order_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch10_order_heatmap.png")
