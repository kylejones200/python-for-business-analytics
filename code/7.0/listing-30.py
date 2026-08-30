"""Create rolling-window features from daily net order value."""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
df = (
    ops.set_index("order_date")["net_value_usd"]
    .resample("D")
    .sum()
    .to_frame(name="sales")
    .reset_index()
    .rename(columns={"order_date": "date"})
)

df["rolling_mean_7"] = df["sales"].rolling(window=7, min_periods=1).mean()
df["rolling_mean_30"] = df["sales"].rolling(window=30, min_periods=1).mean()
df["rolling_std_7"] = df["sales"].rolling(window=7, min_periods=1).std()
df["rolling_min_7"] = df["sales"].rolling(window=7, min_periods=1).min()
df["rolling_max_7"] = df["sales"].rolling(window=7, min_periods=1).max()
df["expanding_mean"] = df["sales"].expanding().mean()

print(
    df[["date", "sales", "rolling_mean_7", "rolling_std_7"]]
    .tail()
    .round(2)
    .to_string(index=False)
)
print("Rolling windows use only data up to the current row.")
