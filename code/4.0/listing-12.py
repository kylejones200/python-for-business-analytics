"""Pearson chi-square test of independence without Yates correction."""

from scipy.stats import chi2_contingency, fisher_exact

# Example 2x2 table used in the hand calculation.
observed = [[25, 15], [20, 30]]

# correction=False matches the uncorrected Pearson statistic of 4.5.
# SciPy's default for a 2x2 table applies Yates's continuity correction.
chi2, p_value, dof, expected = chi2_contingency(observed, correction=False)
print(f"chi-square={chi2:.4f}")
print(f"p-value={p_value:.4f}")
print(f"degrees of freedom={dof}")
print("expected counts:")
print(expected)

# Fisher exact is the fallback when any expected count is below 5.
if expected.min() < 5:
    odds_ratio, fisher_p = fisher_exact(observed)
    print(f"Fisher exact p-value={fisher_p:.4f} odds_ratio={odds_ratio:.4f}")
