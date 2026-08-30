"""Show why a currency-formatted MRR column is not numeric."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
df["mrr_text"] = df["mrr_usd"].map(lambda x: f"${x:,.2f}")
print("mrr_usd dtype:", df["mrr_usd"].dtype)
print("mrr_text dtype:", df["mrr_text"].dtype)
print(df[["mrr_usd", "mrr_text"]].head())
print("numeric columns:", list(df.select_dtypes(include="number").columns))
print("mrr_text is object, so a numeric boxplot will ignore it.")
