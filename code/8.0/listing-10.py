"""Universal kriging as a linear trend plus ordinary kriging of residuals."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import ordinary_krige


import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix

rng = np.random.default_rng(10)
x = rng.uniform(0, 30_000, 50)
y = rng.uniform(0, 30_000, 50)
z = 40 + 0.0012 * x + 0.0007 * y + rng.normal(0, 4, 50)
X = np.column_stack([np.ones(len(x)), x, y])
beta = np.linalg.lstsq(X, z, rcond=None)[0]
resid = z - X @ beta

gx = np.linspace(0, 30_000, 18)
gy = np.linspace(0, 30_000, 18)
surface = np.empty((len(gy), len(gx)))
for i, yy in enumerate(gy):
    for j, xx in enumerate(gx):
        trend = float(np.dot(beta, [1.0, xx, yy]))
        surface[i, j] = trend + ordinary_krige(x, y, resid, xx, yy, 2.0, 12.0, 12_000.0)

print("Linear drift coefficients:", np.round(beta, 6))
print("Residual mean after trend: {:.3f}".format(float(resid.mean())))
print("Universal-kriging grid mean: {:.2f}".format(float(surface.mean())))

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(surface, origin="lower", extent=[0, 30, 0, 30], cmap="viridis")
ax.scatter(x / 1000.0, y / 1000.0, c="white", s=12, edgecolors="k")
ax.set_xlabel("Easting (km)")
ax.set_ylabel("Northing (km)")
ax.set_title("Universal kriging (linear drift + residuals)")
fig.colorbar(im, ax=ax)
fig.tight_layout()
img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "universal_kriging.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/universal_kriging.png")
