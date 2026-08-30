"""Load the packaged customer table and inspect the first rows."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
print("rows:", len(df), "columns:", df.shape[1])
print(df.head())
