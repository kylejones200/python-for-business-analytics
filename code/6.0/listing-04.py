"""Load a persisted churn pipeline and score new customers."""

import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

model_path = Path(__file__).resolve().parent / "ch6_churn_pipeline.joblib"

# Deployment loads a trusted artifact. Rebuild only if that file is missing,
# using the same split and the hyperparameters selected in listing-03.
# Do not load pickle or joblib files from an untrusted source.
if not model_path.exists():
    df = load_frame("business_customers")
    numeric_features = ["mrr_usd", "adoption", "nps", "onboarding_complete"]
    categorical_features = ["segment"]
    X = df[numeric_features + categorical_features].copy()
    X["onboarding_complete"] = X["onboarding_complete"].astype(int)
    y = df["churned"].astype(int)
    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    preprocess = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), numeric_features),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
        ]
    )
    pipeline = Pipeline(
        steps=[
            ("prep", preprocess),
            (
                "clf",
                RandomForestClassifier(
                    n_estimators=100,
                    max_depth=5,
                    min_samples_leaf=4,
                    random_state=42,
                ),
            ),
        ]
    )
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, model_path)
    print(f"Wrote missing trusted pipeline: {model_path.name}")

loaded = joblib.load(model_path)

new_customers = pd.DataFrame(
    {
        "mrr_usd": [15000, 5000, 25000, 2000],
        "adoption": [0.75, 0.25, 0.90, 0.10],
        "nps": [45, 10, 50, -20],
        "onboarding_complete": [1, 0, 1, 0],
        "segment": ["Mid", "SMB", "Enterprise", "SMB"],
    }
)

proba = loaded.predict_proba(new_customers)[:, 1]
for i, churn_prob in enumerate(proba):
    status = "HIGH RISK" if churn_prob >= 0.5 else "Low Risk"
    row = new_customers.iloc[i]
    print(
        f"Customer {i + 1}: MRR=${row['mrr_usd']:,.0f}, "
        f"adoption={row['adoption']:.0%}, NPS={row['nps']}, "
        f"segment={row['segment']}, churn_prob={churn_prob:.1%} ({status})"
    )
print(f"Loaded pipeline from {model_path.name}")
