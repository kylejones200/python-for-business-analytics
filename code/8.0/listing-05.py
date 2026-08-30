"""Fit a spherical variogram model to the experimental curve."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.spatial import distance_matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_zip_points

def spherical_model(h, nugget, sill, range_param):
    h = np.asarray(h, dtype=float)
    gamma = np.empty_like(h)
    mask = h <= range_param
    gamma[mask] = nugget + (sill - nugget) * (
        1.5 * h[mask] / range_param - 0.5 * (h[mask] / range_param) ** 3
    )
    gamma[~mask] = sill
    return gamma

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

ok = n_pairs > 0
params, _ = curve_fit(
    spherical_model,
    lags[ok],
    gamma[ok],
    p0=[float(np.min(gamma[ok])), float(np.var(z)), max_lag / 3.0],
    bounds=([0, 0, 1.0], [float(np.var(z)), 3 * float(np.var(z)), max_lag]),
)
nugget, sill, range_param = params
print("Nugget: {:.1f}".format(nugget))
print("Sill: {:.1f}".format(sill))
print("Range: {:.1f} m ({:.1f} km)".format(range_param, range_param / 1000.0))

h_model = np.linspace(0, max_lag, 100)
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(lags / 1000.0, gamma, s=50, label="Experimental")
ax.plot(h_model / 1000.0, spherical_model(h_model, nugget, sill, range_param), label="Spherical model")
ax.set_xlabel("Lag distance (km)")
ax.set_ylabel("Semivariance")
ax.set_title("Fitted spherical variogram")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "fitted_variogram.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/fitted_variogram.png")
