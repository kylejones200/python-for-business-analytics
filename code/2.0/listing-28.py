"""OLS of MRR on customer segment."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from statsmodels.formula.api import ols

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
model = ols("mrr_usd ~ C(segment)", data=df).fit()
print(model.summary())
print("R-squared: {:.3f}".format(model.rsquared))
print("Enterprise intercept: {:.0f}".format(model.params["Intercept"]))
print("Mid vs Enterprise: {:.0f}".format(model.params["C(segment)[T.Mid]"]))
print("SMB vs Enterprise: {:.0f}".format(model.params["C(segment)[T.SMB]"]))

rows = [
    ["Intercept (Enterprise)", f"{model.params['Intercept']:.0f}"],
    ["Mid vs Enterprise", f"{model.params['C(segment)[T.Mid]']:.0f}"],
    ["SMB vs Enterprise", f"{model.params['C(segment)[T.SMB]']:.0f}"],
    ["R-squared", f"{model.rsquared:.3f}"],
]
fig, ax = plt.subplots(figsize=(6.5, 2.2))
ax.axis("off")
ax.table(cellText=rows, colLabels=["term", "value"], loc="center")
fig.tight_layout()
img = ROOT / "img" / "ch2_mrr_regression.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
