"""Plot the cached 10-year Treasury yield as a second FRED series."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

fred = load_frame("fred_series")
fred["date"] = pd.to_datetime(fred["date"])
series = fred.set_index("date")["DGS10"].dropna()
window = series.loc["2018-01-01":"2022-12-31"]

ax = window.plot(figsize=(10, 4), title="10-year Treasury yield (FRED DGS10)")
ax.set_ylabel("Percent")
plt.tight_layout()

img_dir = ROOT / "img"
img_dir.mkdir(exist_ok=True)
plt.savefig(
    img_dir / "ch7_filtered_timeseries.png", dpi=300, bbox_inches="tight"
)
plt.close()
print("Saved img/ch7_filtered_timeseries.png")
print("2018-2022 min/max:", float(window.min()), float(window.max()))
print("Date of minimum:", window.idxmin().date())
