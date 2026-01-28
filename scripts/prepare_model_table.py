"""Prepare a model-ready table from a lab-style feature table.

Usage:
  python scripts/prepare_model_table.py --in data/processed/feature_table.csv --out data/processed/model_table.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from spacex_landing.pipeline import make_model_table


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", type=str, required=True, help="Input CSV feature table")
    parser.add_argument("--out", type=str, required=True, help="Output model table CSV")
    args = parser.parse_args()

    df = pd.read_csv(args.inp)
    model_table = make_model_table(df)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    model_table.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with shape {model_table.shape}")


if __name__ == "__main__":
    main()
