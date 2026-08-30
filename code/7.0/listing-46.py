"""Plot a three-phase process-improvement control chart."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import generate_kpi_data


import matplotlib.pyplot as plt
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

# Limits come from the baseline phase only so later phases are not used to set
# them.
baseline = data.iloc[:20]
center = float(baseline["KPI_Value"].mean())
std_dev = float(baseline["KPI_Value"].std(ddof=1))
ucl, lcl = center + 3 * std_dev, center - 3 * std_dev

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    data["Date"],
    data["KPI_Value"],
    "o-",
    color="0.20",
    linewidth=1,
    markersize=4,
)
ax.axhline(center, color="0.10", linewidth=1.5, label="Baseline center")
ax.axhline(ucl, color="0.35", linestyle="--", label="Baseline UCL/LCL")
ax.axhline(lcl, color="0.35", linestyle="--")
ax.axvline(data["Date"].iloc[19], color="0.50", linestyle=":")
ax.axvline(data["Date"].iloc[34], color="0.50", linestyle=":")
ax.set_title("Process improvement chart with baseline control limits")
ax.set_xlabel("Date")
ax.set_ylabel("KPI value")
ax.legend()
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(
    img_dir / "ch7_process_improvement_chart.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)
print("Saved img/ch7_process_improvement_chart.png")
print(
    "Baseline center: {:.2f} UCL: {:.2f} LCL: {:.2f}".format(center, ucl, lcl)
)
print(
    "Phase 3 mean: {:.2f}".format(float(data.iloc[35:]["KPI_Value"].mean()))
)
