"""Wrangling and feature engineering."""

from __future__ import annotations
import numpy as np
import pandas as pd

LANDING_SUCCESS = {"True ASDS", "True RTLS", "True Ocean"}

def filter_falcon9(df, booster_col):
    """Keep Falcon 9 launches (remove Falcon 1) based on BoosterVersion column."""
    if booster_col not in df.columns:
        return df.copy()
    return df[df[booster_col] != "Falcon 1"].copy()

def fill_payload_mass_with_mean(df, col):
    """Replace NaNs in PayloadMass with the mean of non-null values."""
    out = df.copy()
    if col in out.columns:
        mean_val = out[col].mean()
        out[col] = out[col].replace(np.nan, mean_val)
    return out

def landing_outcome_label(outcome):
    """Binary label for landing success based on Outcome string."""
    if not isinstance(outcome, str):
        return 0
    return 1 if any(tag in outcome for tag in LANDING_SUCCESS) else 0

def add_class_label(df, outcome_col):
    out = df.copy()
    if outcome_col in out.columns and "Class" not in out.columns:
        out["Class"] = out[outcome_col].apply(landing_outcome_label)
    return out

def one_hot_encode(df, cols):
    out = df.copy()
    present = [c for c in cols if c in out.columns]
    return pd.get_dummies(out, columns=present, drop_first=True)
