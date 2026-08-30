"""Construct unit-level duration, event, and remaining useful life.

RUL at cycle t is true life minus t. A failed unit is observed at its last
cycle (event=1). A still-running unit is right-censored (event=0).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import make_synthetic_turbofan

import numpy as np
import pandas as pd

df = make_synthetic_turbofan()
last = df.sort_values(["unit", "cycle"]).groupby("unit").tail(1).copy()
last["duration"] = last["cycle"]
last["event"] = last["failed"]

print("Unit-level survival table:")
print(last[["unit", "duration", "event", "RUL", "sensor_11"]].head(8).round(2).to_string(index=False))
print("Observed failures:", int(last["event"].sum()), "of", len(last), "units")
print("Median duration:", float(last["duration"].median()))
print("Median RUL at last observed cycle:", float(last["RUL"].median()))
