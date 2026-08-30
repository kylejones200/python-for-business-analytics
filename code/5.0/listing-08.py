"""Prepare gross and net order value for an OLS regression."""

import sys
from pathlib import Path

import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_ops")
X = sm.add_constant(df[["gross_value_usd"]])
y = df["net_value_usd"]

print(f"Observations: {len(df)}")
print(f"Predictors including intercept: {list(X.columns)}")
print(f"Response: net_value_usd")
