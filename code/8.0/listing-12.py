"""Build a matplotlib residual panel for a spatial holdout.

PlotSmith is an optional extra. This listing uses matplotlib so the example
runs from the book environment without another install.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(12)
observed = 200 + rng.normal(0, 20, 40)
predicted = observed + rng.normal(0, 12, 40)
resid = observed - predicted

fig, axes = plt.subplots(1, 2, figsize=(9, 4))
axes[0].scatter(observed, predicted, s=35)
lo, hi = float(min(observed.min(), predicted.min())), float(
    max(observed.max(), predicted.max())
)
axes[0].plot([lo, hi], [lo, hi], "k--")
axes[0].set_xlabel("Observed")
axes[0].set_ylabel("Predicted")
axes[0].set_title("Predicted vs observed")
axes[1].hist(resid, bins=12, color="0.55", edgecolor="white")
axes[1].axvline(0, color="0.10", linestyle="--")
axes[1].set_title("Holdout residuals")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch8_plotsmith_style_residuals.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)
print("Saved img/ch8_plotsmith_style_residuals.png")
print("Residual mean: {:.2f}".format(float(resid.mean())))
print("PlotSmith is optional; matplotlib is enough for these diagnostics.")
