"""Compare MRR by customer segment."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
order = ["Enterprise", "Mid", "SMB"]
data = [df.loc[df["segment"] == s, "mrr_usd"] for s in order]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.boxplot(data, tick_labels=order, showfliers=False)
ax.set_ylabel("Monthly recurring revenue (USD)")
ax.set_title("MRR by customer segment")
fig.tight_layout()

img = ROOT / "img" / "ch2_mrr_by_segment.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
print(df.groupby("segment")["mrr_usd"].median().reindex(order).round(0).to_string())
