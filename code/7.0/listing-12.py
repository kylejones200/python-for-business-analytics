"""Plot the U.S. unemployment rate from the cached FRED file."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("fred_series")
df["date"] = pd.to_datetime(df["date"])
series = df.set_index("date")["UNRATE"].dropna()

ax = series.plot(figsize=(10, 4), title="U.S. civilian unemployment rate (UNRATE)")
ax.set_ylabel("Percent")
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(img_dir / "ch7_timeseries_plot.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved img/ch7_timeseries_plot.png")
print("Peak UNRATE:", float(series.max()), "on", series.idxmax().date())
