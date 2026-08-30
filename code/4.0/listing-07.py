"""Mean adoption gap by segment and region."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
df["adoption_gap"] = 1.0 - df["adoption"]
result = df.groupby(["segment", "region"])["adoption_gap"].mean()
print(result)
