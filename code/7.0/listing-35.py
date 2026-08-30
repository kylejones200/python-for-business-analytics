"""Summarize remaining useful life for failed and censored units."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import make_synthetic_turbofan

import numpy as np
import pandas as pd

df = make_synthetic_turbofan()
last = df.sort_values(["unit", "cycle"]).groupby("unit").tail(1)
failed_rul = last.loc[last["failed"] == 1, "RUL"]
censored_rul = last.loc[last["failed"] == 0, "RUL"]

print("Failed units: last-cycle RUL should be 0. Median:", float(failed_rul.median()))
print("Censored units: last-cycle RUL remains positive. Median:", float(censored_rul.median()))
print("Overall median duration (cycles):", float(last["cycle"].median()))
