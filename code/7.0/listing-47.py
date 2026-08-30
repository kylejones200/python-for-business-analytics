"""Print a control-chart report for the three-phase improvement example."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import generate_kpi_data

import numpy as np
import pandas as pd

phase1 = generate_kpi_data(20, 95, 2.0, "2024-01-01", 11)
rng = np.random.default_rng(12)
phase2 = pd.DataFrame(
    {
        "Date": pd.date_range("2024-01-21", periods=15, freq="D"),
        "KPI_Value": 95 + np.arange(15) * 0.8 + rng.normal(0, 2, 15),
    }
)
phase3 = generate_kpi_data(15, 107, 2.5, "2024-02-05", 13)
data = pd.concat([phase1, phase2, phase3], ignore_index=True)

baseline = data.iloc[:20]
center = float(baseline["KPI_Value"].mean())
std_dev = float(baseline["KPI_Value"].std(ddof=1))
ucl, lcl = center + 3 * std_dev, center - 3 * std_dev
values = data["KPI_Value"]
out = int(((values > ucl) | (values < lcl)).sum())

print("Process improvement report")
print("Period: {} to {}".format(data["Date"].min().date(), data["Date"].max().date()))
print("Baseline center: {:.2f}".format(center))
print("Baseline UCL/LCL: {:.2f} / {:.2f}".format(ucl, lcl))
print("Points beyond baseline limits: {}".format(out))
print("Phase means: {:.2f}, {:.2f}, {:.2f}".format(
    float(data.iloc[:20]["KPI_Value"].mean()),
    float(data.iloc[20:35]["KPI_Value"].mean()),
    float(data.iloc[35:]["KPI_Value"].mean()),
))
print("Capability indices are not computed here because no specification limits were supplied.")
