"""Print Cox coefficients as hazard ratios with confidence intervals."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookhelpers import make_cox_units

import numpy as np
import pandas as pd
from statsmodels.duration.hazard_regression import PHReg

df = make_cox_units()
res = PHReg(df["duration"], df[["sensor_11", "setting_1"]], status=df["event"]).fit(disp=False)
print(res.summary())
hrs = np.exp(res.params)
print("Hazard ratios:")
for name, hr in zip(["sensor_11", "setting_1"], hrs):
    print("  {}: {:.3f}".format(name, float(hr)))
