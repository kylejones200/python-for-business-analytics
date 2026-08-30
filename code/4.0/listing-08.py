"""Welch two-sample t-test of adoption gap by region."""

import sys
from pathlib import Path

from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
df["adoption_gap"] = 1.0 - df["adoption"]

northeast = df.loc[df["region"] == "Northeast", "adoption_gap"]
south = df.loc[df["region"] == "South", "adoption_gap"]

# Equal variances are not assumed for this generic two-group comparison.
result = stats.ttest_ind(northeast, south, equal_var=False)
print(f"n_northeast={len(northeast)} n_south={len(south)}")
print(f"mean_northeast={northeast.mean():.4f} mean_south={south.mean():.4f}")
print(f"statistic={result.statistic:.6f} pvalue={result.pvalue:.6f}")
