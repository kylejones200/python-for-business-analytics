"""Prepare promised versus actual ship days for linear regression."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops_X = ops[["promised_ship_days"]].to_numpy()
ops_y = ops["actual_ship_days"].to_numpy()

ops_X_train, ops_X_test = ops_X[:-200], ops_X[-200:]
ops_y_train, ops_y_test = ops_y[:-200], ops_y[-200:]

print(f"Training set size: {len(ops_X_train)}")
print(f"Test set size: {len(ops_X_test)}")
print(f"Rows: {len(ops)}")
