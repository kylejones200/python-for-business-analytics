"""Report a one-way ANOVA table with the statsmodels formula API."""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

np.random.seed(42)
group1 = np.random.normal(0, 1, 50)
group2 = np.random.normal(0.5, 1, 50)
group3 = np.random.normal(1, 1, 50)

df = pd.DataFrame(
    {
        "value": np.concatenate([group1, group2, group3]),
        "group": np.repeat(["A", "B", "C"], repeats=50),
    }
)

model = ols("value ~ C(group)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table.to_string())
