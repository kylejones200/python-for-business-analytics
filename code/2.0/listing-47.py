"""Impute satisfaction with the median of the same calendar month."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_ops")[["order_date", "satisfaction"]].copy()
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.month
df.loc[10:250, "satisfaction"] = np.nan

df["satisfaction_mean"] = df["satisfaction"].fillna(df["satisfaction"].mean())
df["satisfaction_group"] = df.groupby("month")["satisfaction"].transform(
    lambda s: s.fillna(s.median())
)
print(
    df[
        [
            "order_date",
            "month",
            "satisfaction",
            "satisfaction_mean",
            "satisfaction_group",
        ]
    ]
    .head(12)
    .round(3)
    .to_string(index=False)
)
