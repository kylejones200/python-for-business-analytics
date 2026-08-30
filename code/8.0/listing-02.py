"""Plot projected ZIP centroids joined to catalog income on ZCTA5."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_zip_points

pts = load_zip_points(crs_epsg=3081).sample(80, random_state=8)
x = pts["easting_m"].to_numpy()
y = pts["northing_m"].to_numpy()
z = pts["median_income_usd"].to_numpy()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sc = axes[0].scatter(x / 1000.0, y / 1000.0, c=z, s=40, cmap="viridis")
axes[0].set_xlabel("Easting (km)")
axes[0].set_ylabel("Northing (km)")
axes[0].set_title("Projected ZIP sample")
axes[0].set_aspect("equal", adjustable="box")
fig.colorbar(sc, ax=axes[0], label="Median income (USD)")
axes[1].hist(z, bins=15, color="0.55", edgecolor="white")
axes[1].set_xlabel("Value")
axes[1].set_ylabel("Count")
axes[1].set_title("Value distribution")
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "spatial_data_visualization.png", dpi=300, bbox_inches="tight"
)
plt.close(fig)
print("Saved img/spatial_data_visualization.png")
print(
    "n={}, mean income={:.0f}, coordinates in EPSG:3081 meters".format(
        len(x), float(z.mean())
    )
)
