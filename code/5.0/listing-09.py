"""Fit OLS of net order value on gross order value."""

import sys
from pathlib import Path

import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_ops")
X = sm.add_constant(df[["gross_value_usd"]])
y = df["net_value_usd"]

model = sm.OLS(y, X).fit()
print(model.summary())
print(f"AIC: {model.aic:.2f}")
print(f"BIC: {model.bic:.2f}")
print(f"R-squared: {model.rsquared:.4f}")
