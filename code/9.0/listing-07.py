"""Variance inflation factors for correlated campaign regressors."""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

SEED = 9
rng = np.random.default_rng(SEED)
n = 400
spend = rng.normal(10.0, 2.0, size=n)
awareness = 0.8 * spend + rng.normal(0.0, 0.7, size=n)
support = rng.normal(5.0, 1.5, size=n)
revenue = (
    20.0
    + 1.1 * spend
    + 0.4 * awareness
    + 0.6 * support
    + rng.normal(0.0, 2.0, size=n)
)
X = sm.add_constant(
    pd.DataFrame({"spend": spend, "awareness": awareness, "support": support})
)
vifs = [
    variance_inflation_factor(X.to_numpy(), i) for i in range(1, X.shape[1])
]
print(pd.Series(vifs, index=["spend", "awareness", "support"]).round(3))
print(f"revenue_sd={revenue.std():.3f}")
