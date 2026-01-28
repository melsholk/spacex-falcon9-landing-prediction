"""Train model script.

Expects a *model-ready* table with a binary 'Class' target and only numeric / one-hot features.
You can generate a richer processed table by extending `spacex_landing.wrangle`.

Usage:
    python scripts/train_model.py --data data/processed/model_table.csv --model_out models/best_model.joblib
"""

from __future__ import annotations
import argparse
from pathlib import Path
import joblib
import pandas as pd

from spacex_landing.modeling import train_best_model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--model_out", type=str, default="models/best_model.joblib")
    parser.add_argument("--metrics_out", type=str, default="reports/metrics.json")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    result = train_best_model(df)

    Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(result.best_estimator, args.model_out)

    Path(args.metrics_out).parent.mkdir(parents=True, exist_ok=True)
    import json
    with open(args.metrics_out, "w") as f:
        json.dump({"best_model": result.best_name, **result.metrics}, f, indent=2)

    print(f"Best model: {result.best_name}")
    print(f"Saved model to {args.model_out}")
    print(f"Saved metrics to {args.metrics_out}")

if __name__ == "__main__":
    main()
