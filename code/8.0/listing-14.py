"""Learning curves on a fixed spatial holdout as training size grows."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import ordinary_krige_points


import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix

rng = np.random.default_rng(14)
x = rng.uniform(0, 30_000, 60)
y = rng.uniform(0, 30_000, 60)
z = 70 + 0.0009 * x + rng.normal(0, 5, 60)
test = x >= np.quantile(x, 0.75)
train_pool = np.where(~test)[0]
test_idx = np.where(test)[0]
sizes = [10, 16, 22, 28, 36, 45]
holdout_r2 = []
for n_train in sizes:
    use = train_pool[:n_train]
    pred = ordinary_krige_points(x[use], y[use], z[use], x[test_idx], y[test_idx], 3.0, 20.0, 12_000.0)
    obs = z[test_idx]
    r2 = 1.0 - float(np.sum((obs - pred) ** 2) / np.sum((obs - obs.mean()) ** 2))
    holdout_r2.append(r2)
    print("n_train={} holdout R^2={:.3f}".format(n_train, r2))

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(sizes, holdout_r2, "o-")
ax.axhline(0, color="0.40", linestyle=":")
ax.set_xlabel("Training sample size")
ax.set_ylabel("Spatial-holdout R^2")
ax.set_title("Learning curve on a fixed eastern block")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch8_learning_curves.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch8_learning_curves.png")
print("R^2 can be negative when the holdout block is hard to predict.")
