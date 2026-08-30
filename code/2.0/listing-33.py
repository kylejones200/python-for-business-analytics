"""Summarize NPS and its correlation with MRR."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
print(df["nps"].describe().round(2))
print("mean NPS by segment:")
print(df.groupby("segment")["nps"].mean().round(2))
print("corr(nps, mrr_usd): {:.4f}".format(df["nps"].corr(df["mrr_usd"])))
