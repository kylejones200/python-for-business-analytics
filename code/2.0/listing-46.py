"""Mean and median imputation on operations satisfaction scores."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_ops")[["satisfaction", "discount_rate"]].copy()
df.loc[10:250, "satisfaction"] = np.nan
df.loc[100:175, "discount_rate"] = np.nan

mean_imp = SimpleImputer(strategy="mean")
median_imp = SimpleImputer(strategy="median")
out = pd.DataFrame(
    {
        "satisfaction": df["satisfaction"],
        "satisfaction_mean": mean_imp.fit_transform(
            df[["satisfaction"]]
        ).ravel(),
        "satisfaction_median": median_imp.fit_transform(
            df[["satisfaction"]]
        ).ravel(),
    }
)
print(out.head(12).round(3).to_string(index=False))
print(
    "Missing satisfaction before imputation:",
    int(df["satisfaction"].isna().sum()),
)
