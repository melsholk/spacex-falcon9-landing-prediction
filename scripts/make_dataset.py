"""Make dataset script.

This script is intentionally conservative: it either downloads data via SpaceX API/Wikipedia
or converts existing notebook outputs (CSV/SQLite) into the processed modeling table.

Typical usage:
    python scripts/make_dataset.py --out data/processed/dataset.csv
"""

from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

from spacex_landing.data_collection import collect_launches_flattened
from spacex_landing.wrangle import add_class_label

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, required=True)
    args = parser.parse_args()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = collect_launches_flattened()
    # If you have a richer table from the original labs, replace this with that output.
    # Here we create a minimal binary target based on API success field.
    if "success" in df.columns:
        df["Class"] = df["success"].fillna(False).astype(int)
        df = df.drop(columns=["success"])
    else:
        df = add_class_label(df)

    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with shape {df.shape}")

if __name__ == "__main__":
    main()
