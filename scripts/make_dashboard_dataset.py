from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests


API = "https://api.spacexdata.com/v4"


def _get_json(url, timeout):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def _post_json(url, payload, timeout):
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()


def get_falcon9_rocket_id():
    rockets = _get_json(f"{API}/rockets")
    for r in rockets:
        if r.get("name") == "Falcon 9":
            return r["id"]
    raise RuntimeError("Could not find Falcon 9 rocket ID from /v4/rockets")


def query_falcon9_launches(falcon9_id):
    """
    Uses the /v4/launches/query endpoint to:
      - filter launches to Falcon 9 only
      - populate launchpad and payloads
      - (attempt to) populate core serials for a nicer 'Booster Version Category' field
    """
    body = {
        "query": {
            "rocket": falcon9_id,
            "upcoming": False,
        },
        "options": {
            "pagination": False,
            "select": [
                "flight_number",
                "date_utc",
                "success",
                "payloads",
                "launchpad",
                "cores",
            ],
            "populate": [
                {"path": "launchpad", "select": ["name"]},
                {"path": "payloads", "select": ["mass_kg", "orbit"]},
                # This nested populate is supported by the API's query system in many cases.
                # If it doesn't populate on your environment, we gracefully fall back.
                {"path": "cores.core", "select": ["serial"]},
            ],
            "sort": {"flight_number": "asc"},
        },
    }

    res = _post_json(f"{API}/launches/query", body)
    docs = res.get("docs")
    if not isinstance(docs, list):
        raise RuntimeError("Unexpected response from /v4/launches/query (missing 'docs').")
    return docs


def _sum_payload_mass_kg(payloads):
    masses = []
    for p in payloads or []:
        m = p.get("mass_kg")
        if isinstance(m, (int, float)):
            masses.append(float(m))
    if not masses:
        return None
    return float(sum(masses))


def _pick_orbit(payloads):
    # Dash lab data typically uses a single orbit label;
    # pick the first non-empty orbit value.
    for p in payloads or []:
        o = p.get("orbit")
        if isinstance(o, str) and o.strip():
            return o.strip()
    return None


def _landing_class_from_cores(cores):
    """
    For landing prediction, we want whether the booster landed.
    We compute:
      - 1 if any core has landing_success == True
      - 0 if we have cores and none are True (i.e., False/None)
      - None if cores info is missing
    """
    if not cores:
        return None

    any_true = False
    saw_bool = False

    for c in cores:
        ls = c.get("landing_success")
        if isinstance(ls, bool):
            saw_bool = True
            if ls:
                any_true = True

    if any_true:
        return 1
    if saw_bool:
        return 0
    return None


def _booster_version_category(cores):
    serials = []
    for c in cores or []:
        core_obj = c.get("core")
        # If nested populate worked, core_obj is a dict with 'serial'
        if isinstance(core_obj, dict) and isinstance(core_obj.get("serial"), str):
            serials.append(core_obj["serial"])
        # If populate didn't work, core_obj might be an ID string
        elif isinstance(core_obj, str) and core_obj.strip():
            serials.append(core_obj.strip())

    if not serials:
        return "Unknown"
    # Multiple cores -> join
    return " / ".join(serials)


def build_dashboard_dataframe(launches):
    rows = []
    for L in launches:
        payloads = L.get("payloads") or []
        cores = L.get("cores") or []
        launchpad = L.get("launchpad")

        # launchpad populated => dict with name; else could be ID
        if isinstance(launchpad, dict):
            launch_site = launchpad.get("name")
        else:
            launch_site = launchpad  # id string fallback

        row = {
            "Flight Number": L.get("flight_number"),
            "Date": L.get("date_utc"),
            "Launch Site": launch_site,
            "Payload Mass (kg)": _sum_payload_mass_kg(payloads),
            "Orbit": _pick_orbit(payloads),
            "Booster Version Category": _booster_version_category(cores),
            "class": _landing_class_from_cores(cores),
            "mission_success": L.get("success"),
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    # Light cleanup
    if "Flight Number" in df.columns:
        df["Flight Number"] = pd.to_numeric(df["Flight Number"], errors="coerce").astype("Int64")

    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output CSV path, e.g. data/raw/spacex_launch_dash.csv")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    falcon9_id = get_falcon9_rocket_id()
    launches = query_falcon9_launches(falcon9_id)
    df = build_dashboard_dataframe(launches)

    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df):,} rows to
