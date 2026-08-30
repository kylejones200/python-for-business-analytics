"""Ordinary kriging on a projected grid using a numpy solver.

Kriging variance is the model prediction variance under the variogram and
stationarity assumptions. It is not a generic confidence interval.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import require_dataset


def spherical_gamma(h, nugget, psill, rng):
    h = np.asarray(h, dtype=float)
    out = np.full_like(h, nugget + psill, dtype=float)
    mask = h < rng
    hr = h[mask] / rng
    out[mask] = nugget + psill * (1.5 * hr - 0.5 * hr**3)
    out[h == 0] = 0.0
    return out


def ordinary_krige(x, y, z, x0, y0, nugget, psill, rng):
    n = len(z)
    d_obs = distance_matrix(np.column_stack([x, y]), np.column_stack([x, y]))
    gamma = spherical_gamma(d_obs, nugget, psill, rng)
    A = np.ones((n + 1, n + 1))
    A[:n, :n] = gamma
    A[-1, -1] = 0.0
    d0 = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
    b = np.ones(n + 1)
    b[:n] = spherical_gamma(d0, nugget, psill, rng)
    try:
        w = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        w = np.linalg.lstsq(A, b, rcond=None)[0]
    pred = float(np.dot(w[:n], z))
    var = float(np.dot(w, b))
    return pred, max(var, 0.0)


rng = np.random.default_rng(8)
try:
    import geopandas as gpd

    gdf = gpd.read_file(require_dataset("zip_geometry")).to_crs(3081)
    sample = gdf.sample(60, random_state=8)
    x = sample.geometry.centroid.x.to_numpy()
    y = sample.geometry.centroid.y.to_numpy()
except Exception:
    x = 400_000 + rng.uniform(0, 80_000, size=60)
    y = 1_000_000 + rng.uniform(0, 80_000, size=60)

x0, y0 = x.mean(), y.mean()
z = (
    65000
    + 0.15 * (x - x0)
    + 0.08 * (y - y0)
    + rng.normal(0, 4000, size=len(x))
)
nugget, psill, vrange = 2.0e6, 1.8e7, 35000.0

gx = np.linspace(x.min(), x.max(), 25)
gy = np.linspace(y.min(), y.max(), 25)
pred = np.empty((len(gy), len(gx)))
svar = np.empty_like(pred)
for i, yy in enumerate(gy):
    for j, xx in enumerate(gx):
        pred[i, j], svar[i, j] = ordinary_krige(
            x, y, z, xx, yy, nugget, psill, vrange
        )

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
sc = axes[0].scatter(
    (x - x.min()) / 1000.0, (y - y.min()) / 1000.0, c=z, s=35, cmap="viridis"
)
axes[0].set_title("Sample")
axes[0].set_xlabel("Easting (km)")
axes[0].set_ylabel("Northing (km)")
fig.colorbar(sc, ax=axes[0], fraction=0.046)
im1 = axes[1].imshow(pred, origin="lower", cmap="viridis", aspect="auto")
axes[1].set_title("Ordinary kriging prediction")
fig.colorbar(im1, ax=axes[1], fraction=0.046)
im2 = axes[2].imshow(
    np.sqrt(svar), origin="lower", cmap="Reds", aspect="auto"
)
axes[2].set_title("Model std. deviation")
fig.colorbar(im2, ax=axes[2], fraction=0.046)
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "kriging_results.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/kriging_results.png")
print("Grid mean prediction: {:.0f}".format(float(np.mean(pred))))
print(
    "Kriging variance is model variance, not a generic confidence interval."
)
