"""Compare three group means with a one-way ANOVA."""

import numpy as np
from scipy import stats

np.random.seed(42)
group1 = np.random.normal(0, 1, 50)
group2 = np.random.normal(0.5, 1, 50)
group3 = np.random.normal(1, 1, 50)

f_value, p_value = stats.f_oneway(group1, group2, group3)
print(f"F-value: {f_value:.4f}")
print(f"p-value: {p_value:.4e}")
