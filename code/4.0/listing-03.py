"""Plot the distribution of monthly recurring revenue."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
df["mrr_usd"].hist(bins=30, color="0.35", edgecolor="white")
plt.xlabel("Monthly recurring revenue (USD)")
plt.ylabel("Customers")
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch4_mrr_histogram.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch4_mrr_histogram.png")
