"""Local linear RDD inside a justified bandwidth around the spend cutoff."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

SEED = 9
CUTOFF = 8000.0
BANDWIDTH = 2000.0
TRUE_LOCAL = 22.0

def loyalty_cutoff(rng, n=4000):
    """Next-quarter revenue around a trailing-spend eligibility cutoff."""
    spend = rng.normal(CUTOFF, 2200.0, size=n)
    treated = (spend >= CUTOFF).astype(int)
    centered = spend - CUTOFF
    revenue = (
        210.0
        + 0.018 * centered
        + TRUE_LOCAL * treated
        + 0.004 * centered * treated
        + rng.normal(0.0, 16.0, size=n)
    )
    return pd.DataFrame(
        {"spend": spend, "treated": treated, "centered": centered, "revenue": revenue}
    )

def local_linear(frame, h):
    window = frame.loc[frame["centered"].abs() <= h].copy()
    model = smf.ols("revenue ~ treated + centered + treated:centered", data=window).fit()
    ci = model.conf_int().loc["treated"]
    return {
        "h": h,
        "n": int(len(window)),
        "estimate": float(model.params["treated"]),
        "se": float(model.bse["treated"]),
        "ci_low": float(ci[0]),
        "ci_high": float(ci[1]),
    }

rng = np.random.default_rng(SEED)
df = loyalty_cutoff(rng)

base = local_linear(df, BANDWIDTH)
print("estimand=local average treatment effect at the cutoff")
print(f"bandwidth={base['h']:.0f}")
print(f"n_local={base['n']}")
print(f"rdd_estimate={base['estimate']:.3f}")
print(f"rdd_se={base['se']:.3f}")
print(f"rdd_95ci=({base['ci_low']:.3f}, {base['ci_high']:.3f})")

for h in (1500.0, 2500.0):
    alt = local_linear(df, h)
    print(
        f"sensitivity_h={alt['h']:.0f} estimate={alt['estimate']:.3f} "
        f"ci=({alt['ci_low']:.3f}, {alt['ci_high']:.3f})"
    )

bin_width = 400.0
left = int(((df["centered"] >= -bin_width) & (df["centered"] < 0)).sum())
right = int(((df["centered"] >= 0) & (df["centered"] < bin_width)).sum())
print(f"density_left_bin={left}")
print(f"density_right_bin={right}")
print(f"density_ratio_right_over_left={right / left:.3f}")

local = df.loc[df["centered"].abs() <= BANDWIDTH]
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.scatter(
    local.loc[local["treated"] == 0, "spend"],
    local.loc[local["treated"] == 0, "revenue"],
    s=8,
    alpha=0.35,
    color="0.45",
    label="Below cutoff",
)
ax.scatter(
    local.loc[local["treated"] == 1, "spend"],
    local.loc[local["treated"] == 1, "revenue"],
    s=8,
    alpha=0.35,
    color="0.10",
    label="Above cutoff",
)
ax.axvline(CUTOFF, color="0.2", linestyle="--", linewidth=1)
ax.set_xlabel("Trailing-year spend (USD)")
ax.set_ylabel("Next-quarter revenue (USD)")
ax.set_title("Local RDD window around the loyalty-discount cutoff")
ax.legend()
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch9_rdd_local.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch9_rdd_local.png")
