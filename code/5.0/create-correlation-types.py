"""Create a six-panel figure of association shapes for Chapter 5."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
n = 80
x = rng.uniform(-1.5, 1.5, size=n)

panels = [
    ("Positive linear", x, 1.1 * x + rng.normal(0, 0.25, n)),
    ("Negative linear", x, -1.1 * x + rng.normal(0, 0.25, n)),
    ("Weak linear", x, 0.25 * x + rng.normal(0, 0.9, n)),
    ("Curved", x, x**2 + rng.normal(0, 0.2, n)),
    ("Unrelated", x, rng.normal(0, 1.0, n)),
    ("Outlier-driven", x, 0.05 * x + rng.normal(0, 0.3, n)),
]
panels[5][2][-1] = 4.0
# tuples are immutable for the y we already assigned... panels[5] is fine as we mutated the array.

fig, axes = plt.subplots(2, 3, figsize=(8.2, 5.2), sharex=False, sharey=False)
for ax, (title, xx, yy) in zip(axes.ravel(), panels):
    ax.scatter(xx, yy, s=16, c="0.25", edgecolors="none")
    ax.set_title(title, fontsize=9)
    ax.tick_params(labelsize=7)
fig.supxlabel("Variable X")
fig.supylabel("Variable Y")
fig.tight_layout()

out = Path(__file__).resolve().parents[2] / "img" / "ch5_correlation_types.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved {out}")
