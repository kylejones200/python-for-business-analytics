"""Create first differences and percent changes from daily net value."""

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

df["diff_1"] = df["sales"].diff(1)
df["diff_2"] = df["sales"].diff(2)
df["pct_change_1"] = df["sales"].pct_change(1) * 100

print(df[["date", "sales", "diff_1", "pct_change_1"]].tail().round(2).to_string(index=False))
print("Differencing uses only past values.")
