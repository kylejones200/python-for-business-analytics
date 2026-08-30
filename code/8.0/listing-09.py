"""Predict property values with a spatial block holdout on projected meters."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import ordinary_krige_points


import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix

rng = np.random.default_rng(456)
x = rng.uniform(0, 40_000, 70)
y = rng.uniform(0, 40_000, 70)
value = (
    220
    + 40 * np.exp(-((x - 12_000) ** 2 + (y - 28_000) ** 2) / 8.0e7)
    + 30 * np.exp(-((x - 28_000) ** 2 + (y - 12_000) ** 2) / 7.0e7)
    + rng.normal(0, 12, 70)
)
train = x < np.quantile(x, 0.7)
test = ~train
pred = ordinary_krige_points(x[train], y[train], value[train], x[test], y[test], 20.0, 180.0, 16_000.0)
resid = value[test] - pred
rmse = float(np.sqrt(np.mean(resid**2)))
mae = float(np.mean(np.abs(resid)))
r2 = 1.0 - float(np.sum(resid**2) / np.sum((value[test] - value[test].mean()) ** 2))
print("Spatial holdout RMSE: {:.2f}".format(rmse))
print("Spatial holdout MAE: {:.2f}".format(mae))
print("Spatial holdout R^2: {:.3f} (can be negative)".format(r2))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(x[train] / 1000.0, y[train] / 1000.0, c=value[train], s=30, cmap="RdYlGn", label="Train")
axes[0].scatter(x[test] / 1000.0, y[test] / 1000.0, c=value[test], s=45, marker="^", cmap="RdYlGn", edgecolors="k")
axes[0].set_title("Projected property sample")
axes[0].set_xlabel("Easting (km)")
axes[0].set_ylabel("Northing (km)")
axes[1].scatter(value[test], pred, s=40)
lo, hi = float(min(value[test].min(), pred.min())), float(max(value[test].max(), pred.max()))
axes[1].plot([lo, hi], [lo, hi], "k--")
axes[1].set_title("Block-holdout predictions")
axes[1].set_xlabel("Observed")
axes[1].set_ylabel("Predicted")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "property_value_prediction.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/property_value_prediction.png")
