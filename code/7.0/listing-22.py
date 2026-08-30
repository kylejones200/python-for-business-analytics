"""Plot the empirical distribution of GBM terminal net-value levels.

Under GBM the positive terminal level is lognormal, not normal. The plot
shows the empirical histogram and sample quantiles with no normal overlay.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

rng = np.random.default_rng(42)

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
df = (
    ops.set_index("order_date")["net_value_usd"]
    .resample("D")
    .sum()
    .to_frame(name="net_value_usd")
)

weekly = df["net_value_usd"].resample("W").sum()
weekly = weekly[weekly > 0]
log_returns = np.log(weekly / weekly.shift(1)).dropna()
log_returns = log_returns.clip(-0.8, 0.8)
mu = float(log_returns.mean())
var = float(log_returns.var())
drift = mu - 0.5 * var
sigma = float(log_returns.std())

horizon = 12
n_paths = 1000
start_level = float(weekly.iloc[-1])
shocks = rng.standard_normal((horizon, n_paths))
growth = np.exp(drift + sigma * shocks)
paths = np.empty((horizon + 1, n_paths), dtype=float)
paths[0] = start_level
for t in range(1, horizon + 1):
    paths[t] = paths[t - 1] * growth[t - 1]

terminal = paths[-1]
q10, q50, q90 = np.quantile(terminal, [0.10, 0.50, 0.90])

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(terminal, bins=30, color="0.55", edgecolor="white", density=True)
ax.axvline(q10, color="0.10", linestyle="--", label="10th percentile")
ax.axvline(q50, color="0.10", linestyle="-", label="Median")
ax.axvline(q90, color="0.10", linestyle="--", label="90th percentile")
ax.set_title("Empirical terminal net-value distribution (GBM)")
ax.set_xlabel("Terminal weekly net value (USD)")
ax.set_ylabel("Density")
ax.legend()
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_monte_carlo_histogram.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("Saved img/ch7_monte_carlo_histogram.png")
print("Terminal mean: {:.2f}".format(float(np.mean(terminal))))
print("Terminal median: {:.2f}".format(float(q50)))
print("10th percentile: {:.2f}".format(float(q10)))
print("90th percentile: {:.2f}".format(float(q90)))
print("Terminal GBM levels are lognormal under the model, not normal.")
