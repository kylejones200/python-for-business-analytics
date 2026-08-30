"""Fixed effects, random effects, and a Hausman-style comparison."""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2
from statsmodels.regression.mixed_linear_model import MixedLM

SEED = 9
rng = np.random.default_rng(SEED)

n_entities = 60
n_periods = 8
entity_id = np.repeat(np.arange(n_entities), n_periods)
time_period = np.tile(np.arange(n_periods), n_entities)

promo = rng.normal(size=n_entities * n_periods)
support = rng.normal(size=n_entities * n_periods)
entity_effect = rng.normal(0.0, 1.0, size=n_entities)
time_effect = np.linspace(-0.6, 0.6, n_periods)
revenue = (
    2.0
    + 1.5 * promo
    - 0.7 * support
    + entity_effect[entity_id]
    + time_effect[time_period]
    + rng.normal(0.0, 1.0, size=n_entities * n_periods)
)
df = pd.DataFrame(
    {
        "entity_id": entity_id,
        "time_period": time_period,
        "promo": promo,
        "support": support,
        "revenue": revenue,
    }
)

X = df[["promo", "support"]].copy()
dummies = pd.get_dummies(df["entity_id"], prefix="entity", drop_first=True)
X_fe = sm.add_constant(pd.concat([X, dummies], axis=1)).astype(float)
fe = sm.OLS(df["revenue"], X_fe).fit()
print("estimand=within-entity association of promo and support with revenue")
print(f"fe_promo={float(fe.params['promo']):.3f}")
print(
    f"fe_promo_95ci=({fe.conf_int().loc['promo', 0]:.3f}, "
    f"{fe.conf_int().loc['promo', 1]:.3f})"
)
print(f"fe_support={float(fe.params['support']):.3f}")
print(
    f"fe_support_95ci=({fe.conf_int().loc['support', 0]:.3f}, "
    f"{fe.conf_int().loc['support', 1]:.3f})"
)

X_re = sm.add_constant(df[["promo", "support"]]).astype(float)
re = MixedLM(df["revenue"], X_re, groups=df["entity_id"]).fit(
    reml=False, disp=False
)
print(f"re_promo={float(re.params['promo']):.3f}")
print(f"re_support={float(re.params['support']):.3f}")

b_fe = fe.params[["promo", "support"]].to_numpy()
b_re = re.params[["promo", "support"]].to_numpy()
V_fe = (
    fe.cov_params().loc[["promo", "support"], ["promo", "support"]].to_numpy()
)
V_re = (
    re.cov_params().loc[["promo", "support"], ["promo", "support"]].to_numpy()
)
diff = b_fe - b_re
V = V_fe - V_re
stat = float(diff.T @ np.linalg.pinv(V) @ diff)
pval = float(chi2.sf(stat, df=2))
print(f"hausman_stat={stat:.3f}")
print(f"hausman_df=2")
print(f"hausman_pvalue={pval:.4f}")
print("re_assumption=entity effects uncorrelated with promo and support")
