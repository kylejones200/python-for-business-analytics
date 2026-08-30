"""Onboarding completion by segment as a share of all customers."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
tab = pd.crosstab(df["segment"], df["onboarding_complete"], normalize="all")
print(tab.round(4))
print("completed overall: {:.4f}".format(df["onboarding_complete"].mean()))

fig, ax = plt.subplots(figsize=(7, 2.4))
ax.axis("off")
cols = ["False", "True"]
rows = [
    [idx] + [f"{tab.loc[idx, c]:.3f}" for c in [False, True]]
    for idx in tab.index
]
ax.table(cellText=rows, colLabels=["segment"] + cols, loc="center")
fig.tight_layout()
img = ROOT / "img" / "ch2_crosstab_onboarding.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
