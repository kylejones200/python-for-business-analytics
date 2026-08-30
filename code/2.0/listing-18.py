"""Draw a scatterplot matrix with churn overlaid as colour."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

# churn_prob is the probability the simulator used to draw `churned`, so it is
# not available before the outcome is known. Overlaying it would leak the
# answer into the picture. These four are measures you would hold in advance.
COLUMNS = ["adoption", "nps", "mrr_usd", "employees"]

df = load_frame("business_customers")
frame = df[COLUMNS].copy()
frame["churn"] = df["churned"].astype(int)
print(frame.groupby("churn")[COLUMNS].mean().round(2))

grid = sns.pairplot(frame, hue="churn", diag_kind="hist",
                    plot_kws={"s": 8, "alpha": 0.3})

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
grid.savefig(img_dir / "ch2_pairplot_churn.png", dpi=150, bbox_inches="tight")
plt.close(grid.figure)
print("Saved img/ch2_pairplot_churn.png")
