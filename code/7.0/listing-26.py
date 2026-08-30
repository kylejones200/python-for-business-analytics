"""Run an Augmented Dickey-Fuller test on daily net order value."""

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
    for key, value in result[4].items():
        print("Critical value {}: {:.3f}".format(key, value))
    if result[1] <= 0.05:
        print("Reject the unit-root null at 5%. The series looks stationary.")
    else:
        print(
            "Do not reject the unit-root null at 5%. The series looks "
            "non-stationary."
        )
    return result[1]


ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
series = (
    ops.set_index("order_date")["net_value_usd"]
    .resample("D")
    .sum()
    .asfreq("D")
    .fillna(0.0)
)
test_stationarity(series, "daily net order value")
