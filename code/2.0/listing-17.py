"""Draw a scatterplot matrix of the customer measures."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

# Name the columns rather than taking the first few numeric ones: customer_id
# is an identifier, and plotting it would fill the matrix with meaningless
# panels.
COLUMNS = ["employees", "annual_revenue_usd", "mrr_usd", "adoption", "nps"]

df = load_frame("business_customers")[COLUMNS]
print(df.describe().round(2))

grid = sns.pairplot(df, plot_kws={"s": 8, "alpha": 0.3, "color": "0.35"})

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
grid.savefig(
    img_dir / "ch2_pairplot_measures.png", dpi=150, bbox_inches="tight"
)
plt.close(grid.figure)
print("Saved img/ch2_pairplot_measures.png")
