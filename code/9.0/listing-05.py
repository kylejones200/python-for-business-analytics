"""Synthetic control with pre-treatment fit, donor rationale, and placebos."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SEED = 9
TREAT_START = 2010
TREATED = 1

def fit_weights(y_treated, Y_controls):
    y_treated = np.asarray(y_treated, dtype=float)
    Y_controls = np.asarray(Y_controls, dtype=float)
    n_controls = Y_controls.shape[1]
    w0 = np.full(n_controls, 1.0 / n_controls)

    def obj(w):
        resid = y_treated - (Y_controls @ w)
        return float(resid @ resid)

    res = minimize(
        obj,
        w0,
        method="SLSQP",
        bounds=[(0.0, 1.0)] * n_controls,
        constraints=[{"type": "eq", "fun": lambda w: float(np.sum(w) - 1.0)}],
    )
    if not res.success:
        raise RuntimeError(res.message)
    w = np.clip(res.x, 0.0, 1.0)
    return w / w.sum()

def series_for(df, unit_id, controls, weights):
    treated = (
        df.loc[df["unit_id"] == unit_id]
        .pivot_table(index="year", values="outcome")
        .sort_index()["outcome"]
    )
    control_mat = (
        df.loc[df["unit_id"].isin(controls)]
        .pivot_table(index="year", columns="unit_id", values="outcome")
        .sort_index()
    )
    synth = pd.Series(control_mat.to_numpy() @ weights, index=control_mat.index)
    return treated, synth, treated - synth

rng = np.random.default_rng(SEED)
years = np.arange(2000, 2016)
controls = np.arange(2, 22)
rows = []
for unit in np.concatenate([[TREATED], controls]):
    unit_effect = rng.normal(0.0, 1.0)
    for year in years:
        t = year - years.min()
        base = 5.0 + 0.2 * t + unit_effect + rng.normal(0.0, 0.35)
        treatment = 2.0 if (unit == TREATED and year >= TREAT_START) else 0.0
        rows.append({"unit_id": int(unit), "year": int(year), "outcome": base + treatment})
df = pd.DataFrame(rows)

pre = df["year"] < TREAT_START
y_pre = (
    df.loc[pre & (df["unit_id"] == TREATED)]
    .sort_values("year")["outcome"]
    .to_numpy()
)
Y_pre = (
    df.loc[pre & (df["unit_id"].isin(controls))]
    .pivot_table(index="year", columns="unit_id", values="outcome")
    .sort_index()
    .to_numpy()
)
weights = fit_weights(y_pre, Y_pre)
treated, synth, gap = series_for(df, TREATED, controls, weights)
pre_rmse = float(np.sqrt(np.mean(gap.loc[gap.index < TREAT_START] ** 2)))
post_gap = float(gap.loc[gap.index >= TREAT_START].mean())
print("estimand=treated-unit path versus donor-weighted counterfactual")
print("donor_pool=20 untreated peer markets with the same pre-period window")
print(f"pre_rmse={pre_rmse:.3f}")
print(f"post_mean_gap={post_gap:.3f}")
print("top_weights=")
print(pd.Series(weights, index=controls).sort_values(ascending=False).head(5).round(3))

placebo_abs = []
for unit in controls:
    donors = [u for u in controls if u != unit] + [TREATED]
    y_c = df.loc[pre & (df["unit_id"] == unit)].sort_values("year")["outcome"].to_numpy()
    Y_c = (
        df.loc[pre & (df["unit_id"].isin(donors))]
        .pivot_table(index="year", columns="unit_id", values="outcome")
        .sort_index()
        .to_numpy()
    )
    w_c = fit_weights(y_c, Y_c)
    _, _, gap_c = series_for(df, unit, donors, w_c)
    placebo_abs.append(abs(float(gap_c.loc[gap_c.index >= TREAT_START].mean())))
placebo_abs = np.asarray(placebo_abs)
rank = 1 + int((placebo_abs >= abs(post_gap)).sum())
print(f"placebo_median_abs_post_gap={float(np.median(placebo_abs)):.3f}")
print(f"treated_abs_post_gap_rank={rank}_of_{len(placebo_abs) + 1}")

fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
axes[0].plot(treated.index, treated.values, label="Treated market", linewidth=2)
axes[0].plot(synth.index, synth.values, label="Synthetic control", linewidth=2)
axes[0].axvline(TREAT_START, color="0.2", linestyle="--", linewidth=1)
axes[0].set_ylabel("Outcome")
axes[0].legend()
axes[0].set_title("Synthetic control: treated market versus donor-weighted peers")
axes[1].plot(gap.index, gap.values, color="0.1", linewidth=2)
axes[1].axvline(TREAT_START, color="0.2", linestyle="--", linewidth=1)
axes[1].axhline(0.0, color="0.5", linestyle=":", linewidth=1)
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Gap")
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch9_synthetic_control.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch9_synthetic_control.png")
