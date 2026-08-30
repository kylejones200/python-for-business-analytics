"""Turn industry into indicator columns and summarize them."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
ind = df["industry"].str.get_dummies()
summary = ind.describe().T[["count", "mean"]]
print(summary)

fig, ax = plt.subplots(figsize=(8, 3))
ax.axis("off")
cell = [
    [idx, f"{row['count']:.0f}", f"{row['mean']:.3f}"]
    for idx, row in summary.iterrows()
]
ax.table(
    cellText=cell, colLabels=["industry", "count", "share"], loc="center"
)
fig.tight_layout()
img = ROOT / "img" / "ch2_industry_indicators.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
