"""Load business operations data and build a daily net-value series."""

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
    .to_frame(name="net_value_usd")
)

print(df.head(10).round(2).to_string())
print(
    "Rows:",
    len(df),
    "mean daily net value:",
    round(df["net_value_usd"].mean(), 2),
)
