"""Plot historical daily net order value used for the Monte Carlo example."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
df = (
    ops.set_index("order_date")["net_value_usd"]
    .resample("D")
    .sum()
    .to_frame(name="net_value_usd")
)

df["net_value_usd"].plot(
    figsize=(10, 4),
    title="Daily net order value from {} to {}".format(
        df.index.min().date(), df.index.max().date()
    ),
)
plt.ylabel("USD")
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch7_sales_history.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch7_sales_history.png")
print(df.tail(3).round(2).to_string())
