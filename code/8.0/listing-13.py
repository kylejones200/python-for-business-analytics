"""Kriging performance dashboard on a spatial holdout.

The uncertainty panel uses model standard deviation from the kriging system.
That quantity is not a generic confidence interval.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import ordinary_krige_points


import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.spatial import distance_matrix

rng = np.random.default_rng(13)
x = rng.uniform(0, 30_000, 48)
y = rng.uniform(0, 30_000, 48)
z = 80 + 0.0008 * x + rng.normal(0, 6, 48)
train = x < np.quantile(x, 0.7)
z_pred, stds = ordinary_krige_points(
    x[train],
    y[train],
    z[train],
    x[~train],
    y[~train],
    4.0,
    30.0,
    12_000.0,
    return_std=True,
)
z_test = z[~train]
resid = z_test - z_pred
r2 = 1.0 - float(np.sum(resid**2) / np.sum((z_test - z_test.mean()) ** 2))

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].scatter(z_test, z_pred, s=40)
lo, hi = float(min(z_test.min(), z_pred.min())), float(
    max(z_test.max(), z_pred.max())
)
axes[0].plot([lo, hi], [lo, hi], "k--")
axes[0].set_title("Predicted vs observed")
axes[1].hist(resid, bins=10, color="0.55", edgecolor="white")
axes[1].set_title("Residuals")
stats.probplot(resid, dist="norm", plot=axes[2])
axes[2].set_title("Normal Q-Q")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "performance_dashboard.png", dpi=300, bbox_inches="tight"
)
plt.close(fig)
print("Saved img/performance_dashboard.png")
print("Holdout R^2: {:.3f}".format(r2))
print("Mean model std. deviation: {:.2f}".format(float(stds.mean())))
print("Model variance assumes the variogram and second-order stationarity.")
