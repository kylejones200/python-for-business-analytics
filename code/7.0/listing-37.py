"""Read a survival quantile from the Kaplan-Meier curve."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import kaplan_meier, make_synthetic_turbofan, unit_level

import numpy as np
import pandas as pd

def qth_survival_time(q, times, survival):
    idx = np.where(survival <= q)[0]
    if idx.size == 0:
        return float(times[-1])
    return float(times[int(idx[0])])

units = unit_level(make_synthetic_turbofan())
times, survival = kaplan_meier(units["duration"], units["event"])
q90 = qth_survival_time(0.90, times, survival)
q50 = qth_survival_time(0.50, times, survival)
print("Time when KM survival first drops to 0.90: {:.1f} cycles".format(q90))
print("Time when KM survival first drops to 0.50: {:.1f} cycles".format(q50))
print("Censored units still contribute to the risk set until their last cycle.")
