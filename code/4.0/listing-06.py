"""Create an adoption-gap feature from the adoption score."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
df["adoption_gap"] = 1.0 - df["adoption"]
print(df[["customer_id", "adoption", "adoption_gap"]].head())
print("Mean adoption gap:", float(df["adoption_gap"].mean()))
