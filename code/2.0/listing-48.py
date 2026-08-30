"""Iterative (MICE-style) imputation using related operations columns."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, SimpleImputer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_ops")[["satisfaction", "discount_rate"]].copy()
df.loc[10:250, "satisfaction"] = np.nan
df.loc[100:175, "discount_rate"] = np.nan

cols = ["satisfaction", "discount_rate"]
mean_imp = SimpleImputer(strategy="mean")
iter_imp = IterativeImputer(random_state=42, max_iter=10)
mean_vals = mean_imp.fit_transform(df[cols])
iter_vals = iter_imp.fit_transform(df[cols])
out = pd.DataFrame(
    {
        "satisfaction": df["satisfaction"],
        "satisfaction_mean": mean_vals[:, 0],
        "satisfaction_iter": iter_vals[:, 0],
        "discount_rate": df["discount_rate"],
        "discount_mean": mean_vals[:, 1],
        "discount_iter": iter_vals[:, 1],
    }
)
print(out.head(12).round(3).to_string(index=False))
