"""Compute Moran's I on projected meter coordinates."""

import sys
from pathlib import Path

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
threshold_m = 25000.0
W = ((dist > 0) & (dist <= threshold_m)).astype(float)
z_c = z - z.mean()
I = (len(z) / W.sum()) * np.sum(W * np.outer(z_c, z_c)) / np.sum(z_c**2)

print("Neighbor threshold: {:.0f} m on EPSG:3081".format(threshold_m))
print("Moran's I: {:.4f}".format(float(I)))
if I > 0:
    print("Positive spatial autocorrelation: nearby values are more similar.")
elif I < 0:
    print("Negative spatial autocorrelation: nearby values are dissimilar.")
else:
    print("No spatial autocorrelation under this weights matrix.")
