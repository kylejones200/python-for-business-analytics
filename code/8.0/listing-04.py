"""Compute an experimental variogram on projected meter distances.

Using half the maximum pairwise distance as the largest lag is a common
heuristic, not a universal rule.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_zip_points

pts = load_zip_points(crs_epsg=3081).sample(80, random_state=8)
x = pts["easting_m"].to_numpy()
y = pts["northing_m"].to_numpy()
z = pts["median_income_usd"].to_numpy()

coords = np.column_stack([x, y])
dist = distance_matrix(coords, coords)
iu = np.triu_indices_from(dist, k=1)
distances = dist[iu]
sq_diff = (z[:, None] - z[None, :])[iu] ** 2
max_lag = float(distances.max() / 2.0)
n_lags = 12
bins = np.linspace(0, max_lag, n_lags + 1)
lags = 0.5 * (bins[:-1] + bins[1:])
gamma = np.zeros(n_lags)
n_pairs = np.zeros(n_lags)
for i in range(n_lags):
    mask = (distances >= bins[i]) & (distances < bins[i + 1])
    n_pairs[i] = mask.sum()
    if n_pairs[i] > 0:
        gamma[i] = 0.5 * float(np.mean(sq_diff[mask]))

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(lags / 1000.0, gamma, s=np.maximum(n_pairs, 1), alpha=0.7)
ax.plot(lags / 1000.0, gamma, color="0.35")
ax.axhline(np.var(z), color="0.15", linestyle=":", label="Sample variance")
ax.set_xlabel("Lag distance (km)")
ax.set_ylabel("Semivariance")
ax.set_title("Experimental variogram in projected meters")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "experimental_variogram.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/experimental_variogram.png")
print("Half-max-distance lag cap (heuristic): {:.1f} km".format(max_lag / 1000.0))
print("Pairs in first lag:", int(n_pairs[0]))
