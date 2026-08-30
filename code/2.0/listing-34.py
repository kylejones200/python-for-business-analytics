"""Preview customer-health columns used with NPS."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
view = df[["customer_name", "segment", "nps", "adoption", "mrr_usd"]].head(8)
print(view.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 3))
ax.axis("off")
rows = view.round(2).astype(str).values.tolist()
ax.table(cellText=rows, colLabels=list(view.columns), loc="center")
fig.tight_layout()
img = ROOT / "img" / "ch2_nps_sample.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
