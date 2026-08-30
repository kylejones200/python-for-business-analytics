"""Calculate 3-sigma control limits for a stable KPI series.

Control limits describe expected process variation. They are not
specification limits. Capability indices need both a stable process and
actual customer specification limits.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import generate_kpi_data

import numpy as np
import pandas as pd

def calculate_control_limits(data, column="KPI_Value", sigma_level=3):
    values = data[column]
    center_line = float(values.mean())
    std_dev = float(values.std(ddof=1))
    return {
        "center_line": center_line,
        "ucl": center_line + sigma_level * std_dev,
        "lcl": center_line - sigma_level * std_dev,
        "std_dev": std_dev,
    }

stable_data = generate_kpi_data()
limits = calculate_control_limits(stable_data)
print("Center line: {:.2f}".format(limits["center_line"]))
print("UCL: {:.2f}".format(limits["ucl"]))
print("LCL: {:.2f}".format(limits["lcl"]))
print("Control limits are not specification limits.")
