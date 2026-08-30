"""Augmented Dickey-Fuller test on monthly order volume."""

import sys
from pathlib import Path

from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = ops["order_date"].astype("datetime64[ns]")
ts = ops.set_index("order_date")["order_id"].resample("ME").count()
ts = ts.iloc[1:-1]
result = adfuller(ts)

print(f"n_months={len(ts)}")
print(f"adf_stat={result[0]:.4f}")
print(f"adf_pvalue={result[1]:.4f}")
print(f"used_lag={result[2]}")
if result[1] <= 0.05:
    print("decision=reject unit-root null at 5 percent")
else:
    print("decision=fail to reject unit-root null at 5 percent")
