"""Estimate a Kaplan-Meier survival curve from synthetic turbofan units.

Censoring: a unit still running at the end of follow-up contributes to the
risk set until its last cycle, then drops out without counting as a failure.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import make_synthetic_turbofan, unit_level


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def kaplan_meier(durations, event_observed):
    durations = np.asarray(durations, dtype=float)
    event_observed = np.asarray(event_observed, dtype=int)
    order = np.argsort(durations)
    t = durations[order]
    e = event_observed[order]
    unique_times = np.unique(t[e == 1])
    times = [0.0]
    surv = [1.0]
    s = 1.0
    for ti in unique_times:
        n_at_risk = float(np.sum(t >= ti))
        d_events = float(np.sum((t == ti) & (e == 1)))
        if n_at_risk > 0:
            s *= 1.0 - d_events / n_at_risk
        times.append(float(ti))
        surv.append(float(s))
    return np.array(times), np.array(surv)

units = unit_level(make_synthetic_turbofan())
times, survival = kaplan_meier(units["duration"], units["event"])

fig, ax = plt.subplots(figsize=(8, 5))
ax.step(times, survival, where="post", linewidth=2, label="Kaplan-Meier estimate")
ax.set_xlabel("Cycles")
ax.set_ylabel("Survival probability")
ax.set_title("Kaplan-Meier curve for synthetic turbofan units")
ax.legend()
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_kaplan_meier.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_kaplan_meier.png")
print("Units:", len(units), "events:", int(units["event"].sum()), "censored:", int((units["event"] == 0).sum()))
print("Survival at last event time: {:.3f}".format(float(survival[-1])))
