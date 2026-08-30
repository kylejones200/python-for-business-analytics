"""Illustrate the trade-off between forecasting effort and uncertainty loss."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

effort = np.linspace(0.05, 2.0, 200)
forecast_cost = 18.0 * effort**2
uncertainty_loss = 42.0 * np.exp(-2.2 * effort)
total = forecast_cost + uncertainty_loss
opt = effort[int(np.argmin(total))]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(effort, forecast_cost, linestyle="--", label="Cost of forecasting")
ax.plot(effort, uncertainty_loss, linestyle=":", label="Losses due to uncertainty")
ax.plot(effort, total, linestyle="-", label="Total cost")
ax.axvline(opt, color="0.35", linestyle=":", linewidth=1.2)
ax.set_xlabel("Forecasting effort")
ax.set_ylabel("Cost")
ax.set_title("When more forecasting starts to cost more than it saves")
ax.legend(frameon=False)
fig.tight_layout()

img = Path(__file__).resolve().parents[2] / "img" / "marginal_value_of_information.png"
img.parent.mkdir(exist_ok=True)
fig.savefig(img, dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved", img)
print("Minimum total cost at effort={:.2f}".format(opt))
