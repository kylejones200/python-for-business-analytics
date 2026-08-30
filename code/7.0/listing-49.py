"""Detect retrospective mean-shift change points with binary segmentation.

Binary segmentation sees the whole series. It is not an online detector and
must not be tuned on future values if the goal is predictive evaluation.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import load_safety_data

import numpy as np
import pandas as pd

def sse(values):
    values = np.asarray(values, dtype=float)
    return float(np.sum((values - values.mean()) ** 2)) if len(values) else 0.0

def binary_segmentation(signal, n_bkps=3, min_size=3):
    signal = np.asarray(signal, dtype=float)
    n = len(signal)
    breakpoints = [0, n]
    for _ in range(n_bkps):
        best_gain = 0.0
        best_idx = None
        for i in range(len(breakpoints) - 1):
            start, end = breakpoints[i], breakpoints[i + 1]
            if end - start < 2 * min_size:
                continue
            parent = sse(signal[start:end])
            for tau in range(start + min_size, end - min_size + 1):
                gain = parent - sse(signal[start:tau]) - sse(signal[tau:end])
                if gain > best_gain:
                    best_gain = gain
                    best_idx = tau
        if best_idx is None:
            break
        breakpoints.append(best_idx)
        breakpoints = sorted(breakpoints)
    return breakpoints[1:-1]

df = load_safety_data()
signal = df["RIFR_per_200k"].to_numpy()
change_idx = binary_segmentation(signal, n_bkps=3)
change_years = [int(df["Year"].iloc[i]) for i in change_idx]
print("Detected change-point years:", change_years)
print("These breaks come from a retrospective search over the full series.")
