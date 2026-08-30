"""Compare adoption-gap distributions for two regions."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
df["adoption_gap"] = 1.0 - df["adoption"]

for region, color in [("Northeast", "0.2"), ("South", "0.6")]:
    values = df.loc[df["region"] == region, "adoption_gap"]
    plt.hist(values, bins=20, density=True, alpha=0.55, color=color, label=region)

plt.xlabel("Adoption gap (1 - adoption)")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch4_adoption_gap_by_region.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch4_adoption_gap_by_region.png")
