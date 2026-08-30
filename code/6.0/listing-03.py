"""Tune the churn pipeline on training folds only."""

import sys
from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from bookdata import load_frame

df = load_frame("business_customers")
numeric_features = ["mrr_usd", "adoption", "nps", "onboarding_complete"]
categorical_features = ["segment"]

X = df[numeric_features + categorical_features].copy()
X["onboarding_complete"] = X["onboarding_complete"].astype(int)
y = df["churned"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

preprocess = ColumnTransformer(
    transformers=[
        ("num", SimpleImputer(strategy="median"), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("prep", preprocess),
        ("clf", RandomForestClassifier(random_state=42)),
    ]
)

param_grid = {
    "clf__n_estimators": [50, 100],
    "clf__max_depth": [5, 10, None],
    "clf__min_samples_leaf": [1, 4],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=cv,
    scoring="roc_auc",
    n_jobs=1,
)
grid.fit(X_train, y_train)

best = grid.best_estimator_
y_prob = best.predict_proba(X_test)[:, 1]

model_path = Path(__file__).resolve().parent / "ch6_churn_pipeline.joblib"
joblib.dump(best, model_path)

print(f"Best parameters: {grid.best_params_}")
print(f"Best CV ROC-AUC: {grid.best_score_:.4f}")
print(f"Held-out test ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
print(f"Saved pipeline: {model_path.name}")
