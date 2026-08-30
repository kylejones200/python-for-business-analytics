"""Mean MRR by segment and region."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
pivot = df.pivot_table(
    "mrr_usd", index="segment", columns="region", aggfunc="mean"
)
print(pivot.round(1))

fig, ax = plt.subplots(figsize=(9, 2.8))
ax.axis("off")
cols = list(pivot.columns)
rows = [
    [idx] + [f"{pivot.loc[idx, c]:.0f}" for c in cols] for idx in pivot.index
]
ax.table(cellText=rows, colLabels=[""] + cols, loc="center")
fig.tight_layout()
img = ROOT / "img" / "ch2_pivot_mrr_region.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
