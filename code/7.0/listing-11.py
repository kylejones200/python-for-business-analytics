"""Preview the cached FRED series used in the unemployment example."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("fred_series")
print(df.head().to_string(index=False))
print("Columns:", list(df.columns))
print("Rows:", len(df))
