"""Plot daily net order value from business operations."""

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

plt.figure(figsize=(10, 4))
plt.plot(df.index, df["net_value_usd"], color="0.25", linewidth=1.0)
plt.title("Daily net order value")
plt.ylabel("Net value (USD)")
plt.xlabel("Date")
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(
    img_dir / "ch7_daily_net_order_value.png", dpi=300, bbox_inches="tight"
)
plt.close()
print("Saved img/ch7_daily_net_order_value.png")
print(
    "Days:",
    len(df),
    "min/max:",
    float(df["net_value_usd"].min()),
    float(df["net_value_usd"].max()),
)
