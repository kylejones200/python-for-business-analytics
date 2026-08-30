"""Evaluate the ship-day regression on held-out orders."""

import sys
from pathlib import Path

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

print(f"Coefficient: {regr.coef_[0]:.4f}")
print(f"Variance score (R-squared): {r2_score(ops_y_test, ops_y_pred):.4f}")
