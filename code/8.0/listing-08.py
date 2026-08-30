"""Use ordinary kriging on projected coordinates to rank store sites."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import ordinary_krige


import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix

rng = np.random.default_rng(123)
# 50 km x 50 km projected box. Coordinates are easting/northing in meters.
x = rng.uniform(0, 50_000, 80)
y = rng.uniform(0, 50_000, 80)
demand = 40 + 0.0008 * x + 0.0005 * y + rng.normal(0, 6, 80)
nugget, psill, vrange = 8.0, 40.0, 18_000.0

gx = np.linspace(0, 50_000, 20)
gy = np.linspace(0, 50_000, 20)
surface = np.empty((len(gy), len(gx)))
for i, yy in enumerate(gy):
    for j, xx in enumerate(gx):
        surface[i, j] = ordinary_krige(
            x, y, demand, xx, yy, nugget, psill, vrange
        )

imax = np.unravel_index(np.argmax(surface), surface.shape)
best_x, best_y = gx[imax[1]], gy[imax[0]]

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(
    surface, origin="lower", extent=[0, 50, 0, 50], cmap="RdYlGn", alpha=0.85
)
ax.scatter(
    x / 1000.0, y / 1000.0, s=12, c="0.15", alpha=0.5, label="Customers"
)
ax.scatter(
    [best_x / 1000.0],
    [best_y / 1000.0],
    marker="*",
    s=220,
    c="red",
    label="Highest predicted demand",
)
ax.set_xlabel("Easting (km)")
ax.set_ylabel("Northing (km)")
ax.set_title("Store-site ranking from kriged demand")
ax.legend(loc="upper left")
fig.colorbar(im, ax=ax, label="Predicted purchase frequency")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "store_location_optimization.png", dpi=300, bbox_inches="tight"
)
plt.close(fig)
print("Saved img/store_location_optimization.png")
print(
    "Recommended site: easting={:.1f} km, northing={:.1f} km".format(
        best_x / 1000.0, best_y / 1000.0
    )
)
print("Predicted demand: {:.2f}".format(float(surface[imax])))
