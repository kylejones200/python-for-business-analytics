"""Standardize customer metrics and plot PCA explained variance."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
data = df[
    ["mrr_usd", "adoption", "nps", "employees", "annual_revenue_usd"]
].to_numpy()

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

pca = PCA()
pca.fit(data_scaled)
cumulative = np.cumsum(pca.explained_variance_ratio_)

plt.figure(figsize=(8, 5))
plt.plot(
    np.arange(1, len(cumulative) + 1), cumulative, marker="o", color="0.2"
)
plt.xlabel("Number of components")
plt.ylabel("Cumulative explained variance")
plt.ylim(0, 1.05)
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch5_pca_variance.png", dpi=300, bbox_inches="tight")
plt.close()

print("Saved img/ch5_pca_variance.png")
print("Explained variance ratios:")
print(np.round(pca.explained_variance_ratio_, 4))
print("Cumulative:")
print(np.round(cumulative, 4))
