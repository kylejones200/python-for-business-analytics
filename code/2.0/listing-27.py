"""ANOVA for monthly recurring revenue across customer segments."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
model = ols("mrr_usd ~ C(segment)", data=df).fit()
table = anova_lm(model, typ=2)
print(table)

display = table.copy()
display.index = ["segment", "Residual"]
rows = []
for idx in display.index:
    row = display.loc[idx]
    f_val = "" if pd.isna(row["F"]) else f"{row['F']:.1f}"
    p_val = "" if pd.isna(row["PR(>F)"]) else f"{row['PR(>F)']:.4f}"
    rows.append(
        [idx, f"{row['sum_sq']:.3e}", f"{row['df']:.0f}", f_val, p_val]
    )

fig, ax = plt.subplots(figsize=(8, 2.4))
ax.axis("off")
ax.table(
    cellText=rows,
    colLabels=["", "sum_sq", "df", "F", "PR(>F)"],
    loc="center",
)
fig.tight_layout()
img = ROOT / "img" / "ch2_mrr_anova.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
print(
    "F={:.1f} p={:.4f}".format(
        table.loc["C(segment)", "F"], table.loc["C(segment)", "PR(>F)"]
    )
)
