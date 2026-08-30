"""Customer counts by segment and industry."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
counts = pd.crosstab(df["segment"], df["industry"], margins=True)
print(counts)

fig, ax = plt.subplots(figsize=(9, 2.8))
ax.axis("off")
cols = list(counts.columns)
rows = [
    [idx] + [str(int(counts.loc[idx, c])) for c in cols]
    for idx in counts.index
]
ax.table(cellText=rows, colLabels=[""] + cols, loc="center")
fig.tight_layout()
img = ROOT / "img" / "ch2_pivot_count_industry.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
print("SMB share: {:.3f}".format((df["segment"] == "SMB").mean()))
