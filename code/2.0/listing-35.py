"""Regress MRR on NPS and then on NPS plus segment."""

import sys
from pathlib import Path

from statsmodels.formula.api import ols

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
simple = ols("mrr_usd ~ nps", data=df).fit()
with_segment = ols("mrr_usd ~ nps + C(segment)", data=df).fit()
print("MRR ~ NPS")
print(
    "coef={:.2f} p={:.4f} R2={:.4f}".format(
        simple.params["nps"], simple.pvalues["nps"], simple.rsquared
    )
)
print("MRR ~ NPS + segment")
print(
    "nps coef={:.2f} p={:.4f} R2={:.4f}".format(
        with_segment.params["nps"],
        with_segment.pvalues["nps"],
        with_segment.rsquared,
    )
)
