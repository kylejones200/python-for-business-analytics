"""Plot the MRR distribution on the packaged customer table."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(df["mrr_usd"], bins=40, color="#5E81AC", edgecolor="white")
ax.axvline(
    df["mrr_usd"].mean(), color="#BF616A", linestyle="--", label="Mean"
)
ax.axvline(
    df["mrr_usd"].median(), color="#2E3440", linestyle=":", label="Median"
)
ax.set_xlabel("Monthly recurring revenue (USD)")
ax.set_ylabel("Customers")
ax.set_title("MRR is right-skewed")
ax.legend(frameon=False)
fig.tight_layout()

img = ROOT / "img" / "ch2_mrr_histogram.png"
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img.name)
print(
    "mean={:.0f} median={:.0f} max={:.0f}".format(
        df["mrr_usd"].mean(), df["mrr_usd"].median(), df["mrr_usd"].max()
    )
)
