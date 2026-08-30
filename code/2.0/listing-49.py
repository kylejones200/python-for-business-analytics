"""Keep a missingness indicator before imputing satisfaction."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_ops")[["order_date", "satisfaction"]].copy()
df["order_date"] = pd.to_datetime(df["order_date"])
df.loc[10:250, "satisfaction"] = np.nan
df["satisfaction_missing"] = df["satisfaction"].isna().astype(int)
df["satisfaction_imputed"] = df["satisfaction"].fillna(
    df["satisfaction"].mean()
)
print(
    df[
        [
            "order_date",
            "satisfaction",
            "satisfaction_imputed",
            "satisfaction_missing",
        ]
    ]
    .head(15)
    .round(3)
    .to_string(index=False)
)
print("Missing-indicator rate:", float(df["satisfaction_missing"].mean()))
