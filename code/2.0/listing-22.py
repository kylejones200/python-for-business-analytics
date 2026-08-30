"""Keep the customer columns used in the rest of this section."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
keep = [
    "customer_id",
    "customer_name",
    "industry",
    "segment",
    "region",
    "mrr_usd",
    "nps",
    "adoption",
    "onboarding_complete",
]
view = df[keep]
print(view.dtypes)
print(view.head())
