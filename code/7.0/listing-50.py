"""Plot retrospective change points on the yearly safety series."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import binary_segmentation, load_safety_data


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = load_safety_data()
signal = df["RIFR_per_200k"].to_numpy()
change_idx = binary_segmentation(signal, n_bkps=3)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["Year"], signal, "o-", color="0.20", linewidth=1.2)
for idx in change_idx:
    ax.axvline(df["Year"].iloc[idx], color="0.40", linestyle="--")
    ax.annotate(
        str(int(df["Year"].iloc[idx])),
        (df["Year"].iloc[idx], signal[idx]),
        textcoords="offset points",
        xytext=(4, 8),
    )
ax.set_title("Retrospective change points in yearly RIFR")
ax.set_xlabel("Year")
ax.set_ylabel("RIFR per 200k hours")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_change_points.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_change_points.png")
print("Change-point years:", [int(df["Year"].iloc[i]) for i in change_idx])
