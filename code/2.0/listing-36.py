"""Interpret the NPS slope after segment is already in the model."""

import sys
from pathlib import Path

from statsmodels.formula.api import ols

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
model = ols("mrr_usd ~ nps + C(segment)", data=df).fit()
per_10 = 10.0 * model.params["nps"]
print(
    "NPS coefficient (USD per NPS point): {:.2f}".format(model.params["nps"])
)
print("p-value: {:.4f}".format(model.pvalues["nps"]))
print("USD associated with +10 NPS points: {:.2f}".format(per_10))
print("R-squared: {:.3f}".format(model.rsquared))
print(
    "Segment still dominates. NPS is not a useful MRR predictor in this "
    "sample."
)
