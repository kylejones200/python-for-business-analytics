"""Welch t-test of adoption gap by onboarding completion."""

import sys
from pathlib import Path

from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
df["adoption_gap"] = 1.0 - df["adoption"]

onboarded = df.loc[df["onboarding_complete"], "adoption_gap"]
not_onboarded = df.loc[~df["onboarding_complete"], "adoption_gap"]

result = stats.ttest_ind(onboarded, not_onboarded, equal_var=False)
print(f"n_onboarded={len(onboarded)} n_not_onboarded={len(not_onboarded)}")
print(
    f"mean_onboarded={onboarded.mean():.4f} "
    f"mean_not={not_onboarded.mean():.4f}"
)
print(f"statistic={result.statistic:.6f} pvalue={result.pvalue:.6f}")
