"""Predict Weibull survival probability at a fixed cycle count."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import make_weibull_units

import numpy as np
import pandas as pd
from scipy import stats

df = make_weibull_units()
observed = df.loc[df["event"] == 1, "duration"].to_numpy()
w_shape, w_loc, w_scale = stats.weibull_min.fit(observed, floc=0)
t_star = 160.0
surv = 1.0 - stats.weibull_min(c=w_shape, loc=w_loc, scale=w_scale).cdf(
    t_star
)
print("Weibull survival at t={:.0f}: {:.3f}".format(t_star, float(surv)))
print(
    "That is the model probability a unit is still operating at that cycle."
)
