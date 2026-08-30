"""One-sample proportion test and Wilson interval for customer churn."""

import sys
from pathlib import Path

from statsmodels.stats.proportion import proportion_confint, proportions_ztest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
n = int(len(df))
count = int(df["churned"].sum())
stat, pvalue = proportions_ztest(count, n, value=0.12, alternative="two-sided")
ci_low, ci_high = proportion_confint(count, n, alpha=0.05, method="wilson")

print(f"n={n}")
print(f"churned={count}")
print(f"sample_proportion={count / n:.4f}")
print(f"h0_proportion=0.12")
print(f"z_stat={float(stat):.3f}")
print(f"p_value={float(pvalue):.4f}")
print(f"wilson_95ci=({ci_low:.4f}, {ci_high:.4f})")

on = df.loc[df["onboarding_complete"] == True, "churned"]
off = df.loc[df["onboarding_complete"] == False, "churned"]
z2, p2 = proportions_ztest(
    [int(off.sum()), int(on.sum())],
    [int(len(off)), int(len(on))],
)
print(f"not_onboarded_n={int(len(off))} not_onboarded_churn={float(off.mean()):.4f}")
print(f"onboarded_n={int(len(on))} onboarded_churn={float(on.mean()):.4f}")
print(f"two_proportion_z={float(z2):.3f}")
print(f"two_proportion_p={float(p2):.4f}")
