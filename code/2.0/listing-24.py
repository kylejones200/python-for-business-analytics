"""Strip currency formatting and recast MRR as a float."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
df["mrr_text"] = df["mrr_usd"].map(lambda x: f"${x:,.2f}")
df["mrr_clean"] = (
    df["mrr_text"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)
print(df[["mrr_text", "mrr_clean"]].head())
print("cleaned dtype:", df["mrr_clean"].dtype)
print(
    "matches original:",
    bool((df["mrr_clean"] - df["mrr_usd"]).abs().max() < 1e-8),
)
