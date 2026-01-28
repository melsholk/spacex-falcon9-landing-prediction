"""Data collection utilities.

This project supports two main sources used in the original notebooks:
1) SpaceX REST API (launches, rockets, payloads, launchpads, landpads)
2) Wikipedia table scrape (Falcon 9 / Falcon Heavy launch records)

The functions below are designed to be reproducible and testable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, List
import requests
import pandas as pd

SPACEX_API_BASE = "https://api.spacexdata.com/v4"

@dataclass
class SpaceXAPI:
    session: requests.Session = requests.Session()

    def _get(self, path):
        url = f"{SPACEX_API_BASE}/{path.lstrip('/')}"
        r = self.session.get(url, timeout=30)
        r.raise_for_status()
        return r.json()

    def launches(self):
        return self._get("launches/past")

    def rockets(self):
        return self._get("rockets")

    def payloads(self):
        return self._get("payloads")

    def launchpads(self):
        return self._get("launchpads")

    def landpads(self):
        return self._get("landpads")


def collect_launches_flattened(api = None):
    """Collect past launch data and return a flattened DataFrame.

    """
    api = api or SpaceXAPI()
    launches = api.launches()
    df = pd.json_normalize(launches)

    keep = [
        "flight_number",
        "date_utc",
        "name",
        "success",
        "rocket",
        "payloads",
        "launchpad",
        "cores",
    ]
    cols = [c for c in keep if c in df.columns]
    df = df[cols].copy()
    df.rename(columns={"flight_number": "FlightNumber", "date_utc": "Date"}, inplace=True)
    return df


def save_raw(df, path):
    """Save raw dataframe as CSV."""
    pd.DataFrame(df).to_csv(path, index=False)
