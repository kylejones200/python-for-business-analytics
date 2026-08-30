"""Difference daily net order value and re-test stationarity."""

import sys
from pathlib import Path

import pandas as pd
from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

def test_stationarity(timeseries, title):
    result = adfuller(timeseries.dropna(), autolag="AIC")
    print("ADF test for", title)
    print("ADF statistic: {:.6f}".format(result[0]))
    print("p-value: {:.6f}".format(result[1]))
    if result[1] <= 0.05:
        print("Reject the unit-root null at 5%. The series looks stationary.")
    else:
        print("Do not reject the unit-root null at 5%. The series looks non-stationary.")
    return result[1]

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
series = ops.set_index("order_date")["net_value_usd"].resample("D").sum().asfreq("D").fillna(0.0)
diffed = series.diff().dropna()
print("First difference uses only past values.")
test_stationarity(diffed, "first-differenced daily net order value")
print("Last differenced value: {:.2f}".format(float(diffed.iloc[-1])))
