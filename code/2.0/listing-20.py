"""Draw a correlation heatmap of the measures and the churn outcome."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

MEASURES = ["employees", "annual_revenue_usd", "mrr_usd", "adoption", "nps"]

df = load_frame("business_customers")
frame = df[MEASURES].copy()
frame["churned"] = df["churned"].astype(int)

corr = frame.corr()
print(corr.round(2))

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    linewidth=0.5,
    cmap="rocket",
    vmin=-1,
    vmax=1,
    ax=ax,
)
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch2_correlation_heatmap.png", dpi=150, bbox_inches="tight"
)
plt.close(fig)
print("Saved img/ch2_correlation_heatmap.png")
