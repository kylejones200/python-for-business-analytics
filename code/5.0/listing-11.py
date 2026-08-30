"""Map categorical attributes with multiple correspondence analysis."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame


def multiple_correspondence_analysis(frame, n_components=2):
    """Correspondence analysis on the full indicator matrix (standard MCA)."""
    indicator = pd.get_dummies(frame, drop_first=False).astype(float)
    Z = indicator.to_numpy()
    grand_total = Z.sum()
    P = Z / grand_total
    row_mass = P.sum(axis=1, keepdims=True)
    col_mass = P.sum(axis=0, keepdims=True)
    expected = row_mass @ col_mass
    residuals = P - expected
    row_w = 1.0 / np.sqrt(row_mass)
    col_w = 1.0 / np.sqrt(col_mass)
    standardized = row_w * residuals * col_w
    U, singular_values, _ = np.linalg.svd(standardized, full_matrices=False)
    row_coords = (row_w * U[:, :n_components]) * singular_values[
        :n_components
    ]
    inertia = singular_values**2
    shares = inertia / inertia.sum()
    return row_coords, shares, indicator.columns


df = load_frame("business_customers")
cats = df[["segment", "region", "industry"]].copy()
coords, shares, _ = multiple_correspondence_analysis(cats, n_components=2)

plt.figure(figsize=(8, 6))
for segment, color in [
    ("SMB", "0.15"),
    ("Mid", "0.45"),
    ("Enterprise", "0.70"),
]:
    mask = cats["segment"] == segment
    plt.scatter(
        coords[mask, 0],
        coords[mask, 1],
        s=18,
        alpha=0.7,
        c=color,
        label=segment,
        edgecolors="none",
    )
plt.xlabel("MCA dimension 1")
plt.ylabel("MCA dimension 2")
plt.legend(title="Segment")
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch5_mca.png", dpi=300, bbox_inches="tight")
plt.close()

print("Saved img/ch5_mca.png")
print(f"Dimension 1 inertia share: {shares[0]:.4f}")
print(f"Dimension 2 inertia share: {shares[1]:.4f}")
print(f"Observations: {len(cats)}")
