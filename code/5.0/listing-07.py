"""Plot promised versus actual ship days with the fitted line."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import r2_score

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops_X = ops[["promised_ship_days"]].to_numpy()
ops_y = ops["actual_ship_days"].to_numpy()
ops_X_train, ops_X_test = ops_X[:-200], ops_X[-200:]
ops_y_train, ops_y_test = ops_y[:-200], ops_y[-200:]

regr = linear_model.LinearRegression()
regr.fit(ops_X_train, ops_y_train)
ops_y_pred = regr.predict(ops_X_test)

order = ops_X_test[:, 0].argsort()
plt.figure(figsize=(8, 5))
plt.scatter(ops_X_test, ops_y_test, color="0.25", alpha=0.6, s=22)
plt.plot(ops_X_test[order], ops_y_pred[order], color="0.15", linewidth=2)
plt.xlabel("Promised ship days")
plt.ylabel("Actual ship days")
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(
    img_dir / "ch5_regression_scatter.png", dpi=300, bbox_inches="tight"
)
plt.close()

r2 = r2_score(ops_y_test, ops_y_pred)
print(f"Saved img/ch5_regression_scatter.png")
print(f"Slope: {regr.coef_[0]:.4f}")
print(f"Intercept: {regr.intercept_:.4f}")
print(f"Test R-squared: {r2:.4f}")
