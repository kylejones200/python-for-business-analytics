"""Compare spherical and exponential variograms on a spatial holdout."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix


def gamma_fn(kind, h, nugget, psill, rng):
    h = np.asarray(h, dtype=float)
    if kind == "spherical":
        out = np.full_like(h, nugget + psill, dtype=float)
        mask = h < rng
        hr = h[mask] / rng
        out[mask] = nugget + psill * (1.5 * hr - 0.5 * hr**3)
        out[h == 0] = 0.0
        return out
    out = nugget + psill * (1.0 - np.exp(-h / rng))
    out[h == 0] = 0.0
    return out


def predict(kind, x_tr, y_tr, z_tr, x_te, y_te, nugget, psill, rng):
    preds = []
    for x0, y0 in zip(x_te, y_te):
        n = len(z_tr)
        d_obs = distance_matrix(
            np.column_stack([x_tr, y_tr]), np.column_stack([x_tr, y_tr])
        )
        A = np.ones((n + 1, n + 1))
        A[:n, :n] = gamma_fn(kind, d_obs, nugget, psill, rng)
        A[-1, -1] = 0.0
        d0 = np.sqrt((x_tr - x0) ** 2 + (y_tr - y0) ** 2)
        b = np.ones(n + 1)
        b[:n] = gamma_fn(kind, d0, nugget, psill, rng)
        try:
            w = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            w = np.linalg.lstsq(A, b, rcond=None)[0]
        preds.append(float(np.dot(w[:n], z_tr)))
    return np.asarray(preds)


rng = np.random.default_rng(15)
x = rng.uniform(0, 30_000, 50)
y = rng.uniform(0, 30_000, 50)
z = 75 + 0.0008 * x + rng.normal(0, 6, 50)
train = x < np.quantile(x, 0.7)
results = {}
for kind in ("spherical", "exponential"):
    pred = predict(
        kind,
        x[train],
        y[train],
        z[train],
        x[~train],
        y[~train],
        4.0,
        28.0,
        12_000.0,
    )
    obs = z[~train]
    rmse = float(np.sqrt(np.mean((obs - pred) ** 2)))
    r2 = 1.0 - float(
        np.sum((obs - pred) ** 2) / np.sum((obs - obs.mean()) ** 2)
    )
    results[kind] = {"rmse": rmse, "r2": r2}
    print("{}: RMSE={:.3f} R^2={:.3f}".format(kind, rmse, r2))

fig, axes = plt.subplots(1, 2, figsize=(9, 4))
axes[0].bar(
    results.keys(),
    [r["rmse"] for r in results.values()],
    color="0.55",
    edgecolor="black",
)
axes[0].set_ylabel("RMSE")
axes[0].set_title("Holdout RMSE")
axes[1].bar(
    results.keys(),
    [r["r2"] for r in results.values()],
    color="0.55",
    edgecolor="black",
)
axes[1].axhline(0, color="0.20", linestyle=":")
axes[1].set_ylabel("R^2")
axes[1].set_title("Holdout R^2 (can be negative)")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch8_variogram_model_comparison.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)
print("Saved img/ch8_variogram_model_comparison.png")
