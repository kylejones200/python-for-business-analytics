"""Draw the same matrix as a corner plot, dropping the mirrored panels."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

COLUMNS = ["adoption", "nps", "mrr_usd", "employees"]

df = load_frame("business_customers")
frame = df[COLUMNS].copy()
frame["churn"] = df["churned"].astype(int)

# corner=True keeps only the lower triangle. The upper triangle of a pair plot
# repeats the same panels with the axes swapped, so half the ink carries no
# information the reader has not already seen.
grid = sns.pairplot(frame, hue="churn", diag_kind="hist", corner=True,
                    plot_kws={"s": 8, "alpha": 0.3})
print(f"panels drawn: {sum(ax is not None for ax in grid.axes.flat)}")

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
grid.savefig(img_dir / "ch2_pairplot_corner.png", dpi=150, bbox_inches="tight")
plt.close(grid.figure)
print("Saved img/ch2_pairplot_corner.png")
