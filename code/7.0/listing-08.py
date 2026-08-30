"""Plot a series and its first difference with ACF and PACF diagnostics."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

def ts_panels(series, title, filename):
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    axes[0].plot(series.index, series.values, color="0.20", linewidth=1.0)
    axes[0].set_title(title)
    axes[0].set_ylabel("Value")
    plot_acf(series, ax=axes[1], lags=30)
    plot_pacf(series, ax=axes[2], lags=30, method="ywm")
    fig.tight_layout()
    fig.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)

ops = load_frame("business_ops")
ops["order_date"] = pd.to_datetime(ops["order_date"])
series = ops.set_index("order_date")["net_value_usd"].resample("D").sum().asfreq("D").fillna(0.0)
diffed = series.diff().dropna()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
ts_panels(series, "Original daily net order value", img_dir / "ch7_stationarity_before.png")
ts_panels(diffed, "First difference of daily net order value", img_dir / "ch7_stationarity_after.png")
print("Saved img/ch7_stationarity_before.png")
print("Saved img/ch7_stationarity_after.png")
print("Original last value:", round(float(series.iloc[-1]), 2))
print("Differenced last value:", round(float(diffed.iloc[-1]), 2))
