"""Create the promised-versus-actual ship-day scatter for Chapter 5."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
X = ops[["promised_ship_days"]]
y = ops["actual_ship_days"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(X_test, y_test, s=12, c="0.35", alpha=0.5, label="Held-out orders")
order = X_test["promised_ship_days"].argsort()
ax.plot(
    X_test["promised_ship_days"].iloc[order],
    y_pred[order],
    color="0.1",
    linewidth=2,
    label="Fitted line",
)
ax.set_xlabel("Promised ship days")
ax.set_ylabel("Actual ship days")
ax.legend()
r2 = r2_score(y_test, y_pred)
ax.text(0.05, 0.95, f"R-squared = {r2:.3f}", transform=ax.transAxes, va="top")
fig.tight_layout()

out = ROOT / "img" / "ch5_regression_scatter.png"
fig.savefig(out, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved {out}")
print(f"R-squared={r2:.4f} slope={model.coef_[0]:.4f}")
