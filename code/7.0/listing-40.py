"""Compare Kaplan-Meier with simple parametric survival curves."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import kaplan_meier


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

def make_weibull_units(n_units=80, seed=7):
    rng = np.random.default_rng(seed)
    rows = []
    for unit in range(1, n_units + 1):
        life = float(stats.weibull_min(c=1.6, scale=160).rvs(random_state=rng))
        censor = float(rng.exponential(220))
        duration = min(life, censor)
        event = 1 if life <= censor else 0
        rows.append({"duration": duration, "event": event})
    return pd.DataFrame(rows)

df = make_weibull_units()
km_t, km_s = kaplan_meier(df["duration"], df["event"])
observed = df.loc[df["event"] == 1, "duration"].to_numpy()
exp_scale = float(np.mean(observed))
w_shape, w_loc, w_scale = stats.weibull_min.fit(observed, floc=0)
ln_shape, ln_loc, ln_scale = stats.lognorm.fit(observed, floc=0)

t_grid = np.linspace(0, float(df["duration"].max()) * 1.05, 200)
fig, ax = plt.subplots(figsize=(9, 5))
ax.step(km_t, km_s, where="post", linewidth=2.2, label="Kaplan-Meier")
ax.plot(t_grid, np.exp(-t_grid / exp_scale), label="Exponential")
ax.plot(t_grid, 1.0 - stats.weibull_min(c=w_shape, loc=w_loc, scale=w_scale).cdf(t_grid), label="Weibull")
ax.plot(t_grid, 1.0 - stats.lognorm(s=ln_shape, loc=ln_loc, scale=ln_scale).cdf(t_grid), label="Lognormal")
ax.set_xlabel("Cycles")
ax.set_ylabel("Survival probability")
ax.set_title("Survival model comparison on synthetic turbofan units")
ax.legend()
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_survival_models_comparison.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_survival_models_comparison.png")
print("Weibull shape: {:.3f} scale: {:.1f}".format(w_shape, w_scale))
