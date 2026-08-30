"""Fit and plot the revenue-per-employee regression worked example."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
X = sm.add_constant(df[["employees"]])
model = sm.OLS(df["annual_revenue_usd"], X).fit()
b0 = float(model.params["const"])
b1 = float(model.params["employees"])

print(f"intercept b0 = {b0:,.0f}")
print(f"slope     b1 = {b1:,.2f} USD of annual revenue per employee")
print(f"R-squared    = {model.rsquared:.4f}")
print(
    f"employees range: {int(df['employees'].min())} to "
    f"{int(df['employees'].max())}"
)
print(f"prediction at 250 employees: {b0 + b1 * 250:,.0f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(
    df["employees"],
    df["annual_revenue_usd"] / 1e6,
    s=8,
    alpha=0.35,
    color="0.35",
)
xs = [df["employees"].min(), df["employees"].max()]
ax.plot(xs, [(b0 + b1 * x) / 1e6 for x in xs], color="0.10", linewidth=2)
ax.set_xlabel("Employees")
ax.set_ylabel("Annual revenue (USD millions)")
ax.set_title("Annual revenue against headcount, with the fitted line")
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch5_revenue_employees.png", dpi=300, bbox_inches="tight"
)
plt.close(fig)
print("Saved img/ch5_revenue_employees.png")
