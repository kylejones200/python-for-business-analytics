"""Compare two ARIMA specifications with AIC."""

import sys
from pathlib import Path

from statsmodels.tsa.arima.model import ARIMA

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

ops = load_frame("business_ops")
ops["order_date"] = ops["order_date"].astype("datetime64[ns]")
ts = ops.set_index("order_date")["order_id"].resample("ME").count()
ts = ts.iloc[1:-1]
model1 = ARIMA(ts, order=(1, 1, 1)).fit()
model2 = ARIMA(ts, order=(0, 1, 1)).fit()

print(f"n_months={len(ts)}")
print(f"aic_111={float(model1.aic):.2f}")
print(f"aic_011={float(model2.aic):.2f}")
print(f"preferred={'ARIMA(1,1,1)' if model1.aic <= model2.aic else 'ARIMA(0,1,1)'}")
