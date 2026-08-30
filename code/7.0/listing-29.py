"""Create lag features from daily net order value without using future values."""

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

df["lag_1"] = df["sales"].shift(1)
df["lag_7"] = df["sales"].shift(7)
df["lag_30"] = df["sales"].shift(30)

print(df.head(8).round(2).to_string(index=False))
print("Lag features use only past values.")
