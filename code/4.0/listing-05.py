"""Mean monthly recurring revenue by customer segment."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
result = df.groupby("segment")["mrr_usd"].mean().sort_index()
print(result)
