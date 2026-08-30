"""Compare how three imputation rules change satisfaction spread."""

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
observed = df["satisfaction"]
cols = ["satisfaction", "discount_rate"]
mean_vals = SimpleImputer(strategy="mean").fit_transform(df[cols])[:, 0]
median_vals = SimpleImputer(strategy="median").fit_transform(df[cols])[:, 0]
iter_vals = IterativeImputer(random_state=42, max_iter=10).fit_transform(
    df[cols]
)[:, 0]

methods = {
    "Original (observed)": observed.dropna(),
    "Mean imputation": pd.Series(mean_vals),
    "Median imputation": pd.Series(median_vals),
    "Iterative imputation": pd.Series(iter_vals),
}
for name, series in methods.items():
    print(
        f"{name:24s}  mean={series.mean():.3f}  std={series.std():.3f}  "
        f"n={len(series)}"
    )
