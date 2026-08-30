"""Build a small synthetic CMAPSS-like turbofan table for survival examples.

The official NASA CMAPSS / PHM08 turbofan files are not bundled with this
book. The table below is deterministic synthetic data that follows the same
unit-cycle-sensor layout so the examples run offline.
"""

import numpy as np
import pandas as pd


def make_synthetic_turbofan(n_units=40, seed=7):
    rng = np.random.default_rng(seed)
    rows = []
    for unit in range(1, n_units + 1):
        life = int(rng.integers(90, 220))
        censored = unit % 5 == 0
        observed_end = life if not censored else max(30, int(life * 0.70))
        for t in range(1, observed_end + 1):
            wear = t / float(life)
            rows.append(
                {
                    "unit": unit,
                    "cycle": t,
                    "setting_1": rng.normal(0.0, 0.01),
                    "sensor_4": 1400.0 + 40.0 * wear + rng.normal(0, 3.0),
                    "sensor_11": 47.0 + 8.0 * wear + rng.normal(0, 0.4),
                    "true_life": life,
                    "failed": 0 if censored else 1,
                }
            )
    df = pd.DataFrame(rows)
    df["RUL"] = df["true_life"] - df["cycle"]
    return df


df = make_synthetic_turbofan()
print(df.head().round(2).to_string(index=False))
print("Units:", df["unit"].nunique(), "rows:", len(df))
print("Failed units:", int(df.groupby("unit")["failed"].max().sum()))
print("Censored units:", int((df.groupby("unit")["failed"].max() == 0).sum()))
print(
    "This table is synthetic. Cite NASA/CMAPSS for the original experiment."
)
