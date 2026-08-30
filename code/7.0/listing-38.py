"""Fit a Cox model and interpret coefficients as hazard ratios.

A coefficient beta becomes a hazard ratio exp(beta). A ratio above 1 means
higher hazard (earlier failure) as the covariate increases. The log-log plot
is a simple proportional-hazards diagnostic: roughly parallel curves support
the PH assumption; crossing curves warn against it.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.duration.hazard_regression import PHReg


def make_cox_units(n_units=80, seed=7):
    rng = np.random.default_rng(seed)
    rows = []
    for unit in range(1, n_units + 1):
        sensor = rng.normal(50.0, 4.0)
        life = int(
            np.clip(220 - 2.2 * (sensor - 50.0) + rng.normal(0, 18), 60, 260)
        )
        censored = unit % 5 == 0
        duration = life if not censored else max(30, int(life * 0.70))
        rows.append(
            {
                "duration": duration,
                "event": 0 if censored else 1,
                "sensor_11": sensor,
            }
        )
    return pd.DataFrame(rows)


df = make_cox_units()
res = PHReg(df["duration"], df[["sensor_11"]], status=df["event"]).fit(
    disp=False
)
beta = float(res.params[0])
hr = float(np.exp(beta))
print(res.summary())
print("sensor_11 coefficient: {:.3f}".format(beta))
print("Hazard ratio exp(beta): {:.3f}".format(hr))
print(
    "A 1-unit increase in sensor_11 multiplies the hazard by {:.3f}.".format(
        hr
    )
)

df["high_sensor"] = (df["sensor_11"] >= df["sensor_11"].median()).astype(int)
fig, ax = plt.subplots(figsize=(8, 5))
for label, mask in (
    ("Low sensor_11", df["high_sensor"] == 0),
    ("High sensor_11", df["high_sensor"] == 1),
):
    sub = df.loc[mask]
    order = np.argsort(sub["duration"].to_numpy())
    t = sub["duration"].to_numpy()[order]
    e = sub["event"].to_numpy()[order]
    unique = np.unique(t[e == 1])
    s = 1.0
    times = [1.0]
    loglog = [0.0]
    for ti in unique:
        n_at_risk = float(np.sum(t >= ti))
        d_events = float(np.sum((t == ti) & (e == 1)))
        if n_at_risk > 0:
            s *= 1.0 - d_events / n_at_risk
        if 0 < s < 1:
            times.append(float(ti))
            loglog.append(float(np.log(-np.log(s))))
    ax.plot(np.log(times), loglog, linewidth=2, label=label)
ax.set_xlabel("log(cycles)")
ax.set_ylabel("log(-log(S(t)))")
ax.set_title("Proportional-hazards diagnostic: log-log Kaplan-Meier")
ax.legend()
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch7_cox_partial_effects.png", dpi=300, bbox_inches="tight"
)
plt.close(fig)
print("Saved img/ch7_cox_partial_effects.png")
print("Roughly parallel log-log curves support the PH assumption.")
