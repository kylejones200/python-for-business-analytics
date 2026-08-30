"""Difference-in-differences with a pre-trend event-study diagnostic."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

SEED = 35
TREAT_MONTH = 13
TRUE_EFFECT = 18.0

def loyalty_panel(rng):
    """Region-month revenue after a loyalty-discount rollout in two regions."""
    regions = ["West", "Northeast", "South", "Midwest"]
    treated = {"West", "Northeast"}
    markets = []
    for region in regions:
        for k in range(8):
            markets.append((f"{region}-{k+1}", region, region in treated))
    rows = []
    for market, region, is_treated in markets:
        fe = rng.normal(0.0, 4.0)
        for month in range(1, 25):
            trend = 0.45 * month
            tau = TRUE_EFFECT if (is_treated and month >= TREAT_MONTH) else 0.0
            revenue = 120.0 + fe + trend + tau + rng.normal(0.0, 3.5)
            rows.append(
                {
                    "market": market,
                    "region": region,
                    "month": month,
                    "treated": int(is_treated),
                    "post": int(month >= TREAT_MONTH),
                    "revenue": revenue,
                }
            )
    return pd.DataFrame(rows)

rng = np.random.default_rng(SEED)
df = loyalty_panel(rng)
df["did"] = df["post"] * df["treated"]

did = smf.ols("revenue ~ post + treated + did", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["market"]}
)
est = float(did.params["did"])
ci_low, ci_high = did.conf_int().loc["did"]
print(f"estimand=ATT under parallel trends")
print(f"did_estimate={est:.3f}")
print(f"did_se={float(did.bse['did']):.3f}")
print(f"did_95ci=({ci_low:.3f}, {ci_high:.3f})")
print(f"did_pvalue={float(did.pvalues['did']):.4f}")

df["rel"] = df["month"] - TREAT_MONTH
event = smf.ols(
    "revenue ~ C(rel, Treatment(reference=-1)) * treated + C(market)",
    data=df,
).fit(cov_type="cluster", cov_kwds={"groups": df["market"]})

pre_coefs = []
post_coefs = []
for rel in range(-12, 12):
    if rel == -1:
        continue
    name = f"C(rel, Treatment(reference=-1))[T.{rel}]:treated"
    if name in event.params.index:
        val = float(event.params[name])
        if rel < 0:
            pre_coefs.append((rel, val))
        else:
            post_coefs.append((rel, val))

pre_abs = float(np.mean([abs(v) for _, v in pre_coefs]))
print(f"pretrend_mean_abs_coef={pre_abs:.3f}")
print(f"event_rel_minus3={dict(pre_coefs).get(-3, float('nan')):.3f}")
print(f"event_rel_plus3={dict(post_coefs).get(3, float('nan')):.3f}")

fig, ax = plt.subplots(figsize=(8, 4.5))
rels = [r for r, _ in pre_coefs + [(-1, 0.0)] + post_coefs]
vals = [v for _, v in pre_coefs + [(-1, 0.0)] + post_coefs]
ax.axhline(0.0, color="0.5", linewidth=1)
ax.axvline(-0.5, color="0.3", linestyle="--", linewidth=1)
ax.plot(rels, vals, marker="o", color="0.15")
ax.set_xlabel("Month relative to rollout (omitted: -1)")
ax.set_ylabel("Treat x month coefficient")
ax.set_title("Event-study coefficients for the loyalty-discount rollout")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch9_did_event_study.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch9_did_event_study.png")
