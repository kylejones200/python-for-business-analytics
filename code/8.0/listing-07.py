"""Compare leave-one-out CV with a spatial block holdout.

LOO-CV is educational but optimistic when nearby points leak spatial
information. A spatial/block holdout is the preferred deployment test.
Held-out R^2 can be negative.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import spherical_gamma

from bookdata import load_zip_points

def ordinary_krige_points(x_tr, y_tr, z_tr, x_te, y_te, nugget, psill, rng):
    preds = []
    for x0, y0 in zip(x_te, y_te):
        n = len(z_tr)
        d_obs = distance_matrix(np.column_stack([x_tr, y_tr]), np.column_stack([x_tr, y_tr]))
        A = np.ones((n + 1, n + 1))
        A[:n, :n] = spherical_gamma(d_obs, nugget, psill, rng)
        A[-1, -1] = 0.0
        d0 = np.sqrt((x_tr - x0) ** 2 + (y_tr - y0) ** 2)
        b = np.ones(n + 1)
        b[:n] = spherical_gamma(d0, nugget, psill, rng)
        try:
            w = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            w = np.linalg.lstsq(A, b, rcond=None)[0]
        preds.append(float(np.dot(w[:n], z_tr)))
    return np.asarray(preds)

def metrics(obs, pred):
    resid = obs - pred
    mae = float(np.mean(np.abs(resid)))
    rmse = float(np.sqrt(np.mean(resid**2)))
    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((obs - obs.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return mae, rmse, r2

pts = load_zip_points(crs_epsg=3081).sample(40, random_state=8)
x = pts["easting_m"].to_numpy()
y = pts["northing_m"].to_numpy()
z = pts["median_income_usd"].to_numpy()
nugget, psill, vrange = 2.0e6, 1.8e7, 35000.0

loo_pred = np.empty(len(z))
for i in range(len(z)):
    loo_pred[i] = ordinary_krige_points(
        np.delete(x, i), np.delete(y, i), np.delete(z, i),
        np.array([x[i]]), np.array([y[i]]), nugget, psill, vrange
    )[0]
loo_mae, loo_rmse, loo_r2 = metrics(z, loo_pred)

# Spatial holdout: eastern third of the sample.
east_cut = np.quantile(x, 0.67)
train = x < east_cut
test = ~train
block_pred = ordinary_krige_points(x[train], y[train], z[train], x[test], y[test], nugget, psill, vrange)
blk_mae, blk_rmse, blk_r2 = metrics(z[test], block_pred)

print("LOO-CV  MAE={:.0f} RMSE={:.0f} R^2={:.3f}".format(loo_mae, loo_rmse, loo_r2))
print("Block holdout MAE={:.0f} RMSE={:.0f} R^2={:.3f}".format(blk_mae, blk_rmse, blk_r2))
print("R^2 can be negative on held-out predictions.")

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(z, loo_pred, s=30)
axes[0].plot([z.min(), z.max()], [z.min(), z.max()], "k--")
axes[0].set_title("LOO-CV (optimistic)")
axes[0].set_xlabel("Observed")
axes[0].set_ylabel("Predicted")
axes[1].scatter(z[test], block_pred, s=40)
lo, hi = float(z[test].min()), float(z[test].max())
axes[1].plot([lo, hi], [lo, hi], "k--")
axes[1].set_title("Spatial block holdout")
axes[1].set_xlabel("Observed")
axes[1].set_ylabel("Predicted")
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "kriging_crossvalidation.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/kriging_crossvalidation.png")
