"""Define raw churn features and a stratified train/test split."""

import sys
from pathlib import Path

from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
feature_cols = [
    "mrr_usd",
    "adoption",
    "nps",
    "onboarding_complete",
    "segment",
]
X = df[feature_cols].copy()
X["onboarding_complete"] = X["onboarding_complete"].astype(int)
y = df["churned"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Rows: {len(df)}")
print(f"Training rows: {len(X_train)}")
print(f"Test rows: {len(X_test)}")
print(f"Training churn rate: {y_train.mean():.4f}")
print(f"Test churn rate: {y_test.mean():.4f}")
