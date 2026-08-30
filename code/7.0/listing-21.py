"""Simulate future daily net-value paths with geometric Brownian motion.

GBM is an illustrative stochastic model, not a generally valid sales process.
It assumes independent log-returns, constant drift and volatility, and no
zero or negative levels. Daily net order value can be zero, so the simulation
uses only strictly positive days and a small floor.
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

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(paths, color="0.55", linewidth=0.4, alpha=0.25)
ax.set_title("{} GBM paths for daily net order value".format(n_paths))
ax.set_xlabel("Weeks ahead")
ax.set_ylabel("Weekly net value (USD)")
fig.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_monte_carlo_paths.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("Saved img/ch7_monte_carlo_paths.png")
print("Start level: {:.2f}".format(start_level))
print("Estimated weekly drift: {:.5f}".format(drift))
print("Estimated weekly sigma: {:.5f}".format(sigma))
print("Terminal median: {:.2f}".format(float(np.median(paths[-1]))))
print("GBM assumptions: constant mu/sigma, independent log-returns, strictly positive levels.")
print("This is illustrative. Sales are not generally a GBM.")
