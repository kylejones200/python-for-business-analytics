"""Indicator kriging: probability of exceeding a threshold."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import ordinary_krige


import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix

rng = np.random.default_rng(11)
x = rng.uniform(0, 30_000, 55)
y = rng.uniform(0, 30_000, 55)
z = 50 + 0.0009 * x + rng.normal(0, 8, 55)
threshold = float(np.median(z))
indicator = (z > threshold).astype(float)

gx = np.linspace(0, 30_000, 18)
gy = np.linspace(0, 30_000, 18)
prob = np.empty((len(gy), len(gx)))
for i, yy in enumerate(gy):
    for j, xx in enumerate(gx):
        prob[i, j] = ordinary_krige(
            x, y, indicator, xx, yy, 0.02, 0.20, 12_000.0, clip=(0.0, 1.0)
        )

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(
    prob,
    origin="lower",
    extent=[0, 30, 0, 30],
    cmap="RdYlGn_r",
    vmin=0,
    vmax=1,
)
ax.scatter(
    x / 1000.0, y / 1000.0, c=indicator, cmap="RdYlGn_r", s=28, edgecolors="k"
)
ax.set_xlabel("Easting (km)")
ax.set_ylabel("Northing (km)")
ax.set_title("Indicator kriging P(value > median)")
fig.colorbar(im, ax=ax, label="Probability")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "indicator_kriging.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/indicator_kriging.png")
print("Threshold: {:.2f}".format(threshold))
print(
    "Mean predicted exceedance probability: {:.3f}".format(float(prob.mean()))
)
