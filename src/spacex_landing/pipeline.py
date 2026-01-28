"""High-level helpers to turn a lab-style table into a model-ready table."""

from __future__ import annotations

import pandas as pd

from spacex_landing.wrangle import (
    add_class_label,
    fill_payload_mass_with_mean,
    filter_falcon9,
    one_hot_encode,
)

DEFAULT_CATEGORICAL = [
    "Orbit",
    "LaunchSite",
    "LandingPad",
    "Serial",
    "BoosterVersion",
]

DEFAULT_BINARY = ["GridFins", "Reused", "Legs"]


def make_model_table(df):
    """Create a model-ready table with one-hot encoded categoricals and a `Class` target."""
    out = df.copy()

    out = filter_falcon9(out, booster_col="BoosterVersion")
    out = fill_payload_mass_with_mean(out, col="PayloadMass")

    if "Class" not in out.columns and "Outcome" in out.columns:
        out = add_class_label(out, outcome_col="Outcome")

    for b in DEFAULT_BINARY:
        if b in out.columns:
            out[b] = out[b].astype(int)

    cat_cols = [c for c in DEFAULT_CATEGORICAL if c in out.columns]
    out = one_hot_encode(out, cat_cols)

    # Keep only numeric columns + Class
    numeric_cols = out.select_dtypes(include=["number", "bool"]).columns.tolist()
    if "Class" in out.columns and "Class" not in numeric_cols:
        numeric_cols.append("Class")

    return out[numeric_cols].copy()
