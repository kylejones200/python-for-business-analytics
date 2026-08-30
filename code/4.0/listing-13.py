"""Interpret a chi-square test after choosing alpha in advance."""

import numpy as np
from scipy.stats import chi2_contingency, fisher_exact

observed = np.array([[25, 15], [20, 30]])
alpha = 0.05

chi2, p_value, dof, expected = chi2_contingency(observed, correction=False)
print(f"chi-square={chi2:.4f}")
print(f"p-value={p_value:.4f}")
print(f"degrees of freedom={dof}")
print("expected counts:")
print(expected)

if (expected < 5).any():
    _, fisher_p = fisher_exact(observed)
    print(f"Sparse table: use Fisher exact p-value={fisher_p:.4f}")
elif p_value <= alpha:
    print("Reject the null of independence at the preselected alpha.")
else:
    print("Fail to reject the null of independence at the preselected alpha.")
