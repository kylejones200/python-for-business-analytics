"""Choose a retrospective change-point count by a simple penalty.

The penalty trades fit against extra breaks. This is still a full-sample
segmentation. It is not an online monitoring rule and does not use a
held-out future window.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import binary_segmentation, load_safety_data, sse

import numpy as np
import pandas as pd

df = load_safety_data()
signal = df["RIFR_per_200k"].to_numpy()
penalty = 8.0
best = (np.inf, 0, [])
for k in range(0, 6):
    bounds = binary_segmentation(signal, n_bkps=k, include_bounds=True)
    rss = sum(sse(signal[a:b]) for a, b in zip(bounds[:-1], bounds[1:]))
    score = rss + penalty * k
    years = [int(df["Year"].iloc[i]) for i in bounds[1:-1]]
    print(
        "k={}: RSS={:.2f} score={:.2f} years={}".format(k, rss, score, years)
    )
    if score < best[0]:
        best = (score, k, years)

print("Penalty-selected k={}: years={}".format(best[1], best[2]))
print(
    "This selection uses the full series. Do not treat it as a forecast test."
)
