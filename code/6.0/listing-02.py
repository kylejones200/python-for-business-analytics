"""Fit a Random Forest churn pipeline and score the held-out test set."""

import sys
from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
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
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
    ]
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_auc = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="roc_auc")
cv_f1 = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1")

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

model_path = Path(__file__).resolve().parent / "ch6_churn_pipeline.joblib"
joblib.dump(pipeline, model_path)

print(f"CV ROC-AUC: {cv_auc.mean():.4f} (sd {cv_auc.std():.4f})")
print(f"CV F1: {cv_f1.mean():.4f} (sd {cv_f1.std():.4f})")
print(f"Test ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
print("Test classification report:")
print(classification_report(y_test, y_pred, digits=3))
print("Confusion matrix (rows=true, cols=predicted):")
print(confusion_matrix(y_test, y_pred))
print(f"Saved pipeline: {model_path.name}")
