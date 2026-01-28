"""Model training and evaluation."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Tuple
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

MODELS = {
    "logreg": LogisticRegression(max_iter=5000),
    "svm": SVC(probability=True),
    "dt": DecisionTreeClassifier(),
    "knn": KNeighborsClassifier(),
}

PARAM_GRIDS = {
    "logreg": {"clf__C": [0.1, 1.0, 10.0]},
    "svm": {"clf__C": [0.1, 1.0, 10.0], "clf__gamma": ["scale", "auto"]},
    "dt": {"clf__max_depth": [None, 3, 5, 10], "clf__min_samples_split": [2, 5, 10]},
    "knn": {"clf__n_neighbors": [3, 5, 7, 9]},
}

@dataclass
class TrainResult:
    best_name: str
    best_estimator: Any
    metrics: Dict[str, Any]

def split_xy(df, target):
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")
    X = df.drop(columns=[target])
    y = df[target].astype(int)
    return X, y

def train_best_model(
    df: pd.DataFrame,
    target: str = "Class",
    test_size: float = 0.2,
    random_state: int = 42,
) -> TrainResult:
    X, y = split_xy(df, target=target)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

    best_overall = None
    best_name = None
    best_acc = -1.0
    best_metrics = {}

    for name, clf in MODELS.items():
        pipe = Pipeline([("scaler", StandardScaler(with_mean=False)), ("clf", clf)])
        grid = GridSearchCV(pipe, PARAM_GRIDS[name], cv=5, n_jobs=-1)
        grid.fit(X_train, y_train)
        pred = grid.predict(X_test)

        metrics = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "f1": float(f1_score(y_test, pred)),
            "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
            "report": classification_report(y_test, pred, output_dict=True),
        }
        if metrics["accuracy"] > best_acc:
            best_acc = metrics["accuracy"]
            best_overall = grid.best_estimator_
            best_name = name
            best_metrics = metrics

    return TrainResult(best_name=best_name, best_estimator=best_overall, metrics=best_metrics)
