"""Flag long runs and points beyond control limits."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import calculate_control_limits, generate_kpi_data

import numpy as np
import pandas as pd

def longest_run(mask):
    longest = current = 0
    for flag in mask:
        current = current + 1 if flag else 0
        longest = max(longest, current)
    return longest

data = generate_kpi_data()
limits = calculate_control_limits(data)
values = data["KPI_Value"]
out = int(((values > limits["ucl"]) | (values < limits["lcl"])).sum())
run_above = longest_run(values > limits["center_line"])
run_below = longest_run(values < limits["center_line"])
print("Total points:", len(data))
print("Beyond control limits:", out)
print("Longest run above center:", run_above)
print("Longest run below center:", run_below)
if out == 0 and run_above <= 8 and run_below <= 8:
    print("No Western Electric run or limit signal in this sample.")
else:
    print("At least one run or limit signal is present.")
