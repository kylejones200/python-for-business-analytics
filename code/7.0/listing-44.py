"""Plot a control chart with 3-sigma limits for a stable KPI."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import calculate_control_limits, generate_kpi_data


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = generate_kpi_data()
limits = calculate_control_limits(data)
out_of_control = (data["KPI_Value"] > limits["ucl"]) | (
    data["KPI_Value"] < limits["lcl"]
)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    data["Date"],
    data["KPI_Value"],
    "o-",
    color="0.20",
    linewidth=1,
    markersize=4,
)
ax.axhline(
    limits["center_line"], color="0.10", linewidth=1.5, label="Center line"
)
ax.axhline(limits["ucl"], color="0.35", linestyle="--", label="UCL")
ax.axhline(limits["lcl"], color="0.35", linestyle="--", label="LCL")
if out_of_control.any():
    ax.scatter(
        data.loc[out_of_control, "Date"],
        data.loc[out_of_control, "KPI_Value"],
        color="0.05",
        s=80,
        marker="x",
        linewidths=2,
        label="Beyond control limits",
    )
ax.set_title("Stable-process control chart")
ax.set_xlabel("Date")
ax.set_ylabel("KPI value")
ax.legend()
fig.tight_layout()

img_dir = Path(__file__).resolve().parents[2] / "img"
img_dir.mkdir(exist_ok=True)
fig.savefig(img_dir / "ch7_control_chart.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved img/ch7_control_chart.png")
print("Out-of-control points:", int(out_of_control.sum()))
