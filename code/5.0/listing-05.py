"""Fit a linear regression of actual ship days on promised ship days."""

import sys
from pathlib import Path

from sklearn import linear_model

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops_X = ops[["promised_ship_days"]].to_numpy()
ops_y = ops["actual_ship_days"].to_numpy()
ops_X_train, ops_X_test = ops_X[:-200], ops_X[-200:]
ops_y_train = ops_y[:-200]

regr = linear_model.LinearRegression()
regr.fit(ops_X_train, ops_y_train)
ops_y_pred = regr.predict(ops_X_test)

print(f"Intercept: {regr.intercept_:.4f}")
print(f"Coefficient: {regr.coef_[0]:.4f}")
print(f"Predictions on test rows: {len(ops_y_pred)}")
