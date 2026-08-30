"""Compare L2 and L1 retrospective binary segmentation."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import binary_segmentation, load_safety_data

import numpy as np
import pandas as pd

def cost(values, kind="l2"):
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return 0.0
    if kind == "l2":
        return float(np.sum((values - values.mean()) ** 2))
    return float(np.sum(np.abs(values - np.median(values))))

df = load_safety_data()
signal = df["RIFR_per_200k"].to_numpy()
for kind in ("l2", "l1"):
    idx = binary_segmentation(signal, n_bkps=3, kind=kind)
    years = [int(df["Year"].iloc[i]) for i in idx]
    print("{} years: {}".format(kind.upper(), years))
print("Agreement across costs is a robustness check, not a predictive test.")
