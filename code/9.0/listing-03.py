"""Explicit two-stage least squares for an endogenous loyalty discount."""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

SEED = 9
TRUE_EFFECT = 1.60


def loyalty_iv(rng, n=2500):
    """Promotions shift discount depth; demand shocks confound OLS."""
    competitor_promo = rng.normal(0.0, 1.0, size=n)
    demand_shock = rng.normal(0.0, 1.0, size=n)
    accounts = rng.normal(0.0, 1.0, size=n)
    discount = (
        8.0
        + 2.4 * competitor_promo
        + 1.1 * demand_shock
        + 0.3 * accounts
        + rng.normal(0.0, 1.0, size=n)
    )
    revenue = (
        40.0
        + TRUE_EFFECT * discount
        + 3.0 * demand_shock
        + 0.8 * accounts
        + rng.normal(0.0, 4.0, size=n)
    )
    return pd.DataFrame(
        {
            "revenue": revenue,
            "discount": discount,
            "competitor_promo": competitor_promo,
            "accounts": accounts,
        }
    )


def twosls(y, X, Z):
    """2SLS with residuals formed from the original endogenous regressors."""
    Pz = Z @ np.linalg.inv(Z.T @ Z) @ Z.T
    Xhat = Pz @ X
    beta = np.linalg.inv(Xhat.T @ Xhat) @ Xhat.T @ y
    resid = y - X @ beta
    n, k = X.shape
    sigma2 = float(resid.T @ resid / (n - k))
    vcov = sigma2 * np.linalg.inv(Xhat.T @ Xhat)
    se = np.sqrt(np.diag(vcov))
    return beta, se


rng = np.random.default_rng(SEED)
df = loyalty_iv(rng)

ols = smf.ols("revenue ~ discount + accounts", data=df).fit()
print(
    "estimand=LATE for accounts whose discount moves with competitor "
    "promotions"
)
print(f"ols_discount={float(ols.params['discount']):.3f}")
print(
    f"ols_95ci=({ols.conf_int().loc['discount', 0]:.3f}, "
    f"{ols.conf_int().loc['discount', 1]:.3f})"
)

first = smf.ols("discount ~ competitor_promo + accounts", data=df).fit()
restricted = smf.ols("discount ~ accounts", data=df).fit()
f_excl = (restricted.ssr - first.ssr) / 1 / (first.ssr / first.df_resid)
print(f"first_stage_coef={float(first.params['competitor_promo']):.3f}")
print(f"first_stage_f={float(f_excl):.2f}")

y = df["revenue"].to_numpy()
X = sm.add_constant(df[["discount", "accounts"]]).to_numpy()
Z = sm.add_constant(df[["competitor_promo", "accounts"]]).to_numpy()
beta, se = twosls(y, X, Z)
est = float(beta[1])
ci_low = est - 1.96 * float(se[1])
ci_high = est + 1.96 * float(se[1])
print(f"iv_discount={est:.3f}")
print(f"iv_se={float(se[1]):.3f}")
print(f"iv_95ci=({ci_low:.3f}, {ci_high:.3f})")
print(f"weak_instrument_heuristic_F10={'pass' if f_excl >= 10 else 'fail'}")
