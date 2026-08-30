"""Summarize mean RIFR in each retrospective segment."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import binary_segmentation, load_safety_data

import numpy as np
import pandas as pd

df = load_safety_data()
signal = df["RIFR_per_200k"].to_numpy()
bounds = binary_segmentation(signal, n_bkps=3, include_bounds=True)
print("Segment summaries (retrospective):")
for start, end in zip(bounds[:-1], bounds[1:]):
    piece = df.iloc[start:end]
    print(
        "  {}-{}: n={}, mean={:.2f}, sd={:.2f}".format(
            int(piece["Year"].iloc[0]),
            int(piece["Year"].iloc[-1]),
            len(piece),
            float(piece["RIFR_per_200k"].mean()),
            (
                float(piece["RIFR_per_200k"].std(ddof=1))
                if len(piece) > 1
                else 0.0
            ),
        )
    )
