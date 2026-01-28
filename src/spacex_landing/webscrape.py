"""Web scraping utilities for Wikipedia launch tables."""

from __future__ import annotations
import pandas as pd
import requests
from bs4 import BeautifulSoup

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"

def scrape_wikipedia_launch_table(url):
    """Scrape Falcon 9/Heavy launch records table(s) from Wikipedia.

    Note: Wikipedia tables change over time. This function aims to be resilient but may require updates.
    """
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    tables = soup.find_all("table", class_="wikitable")
    if not tables:
        raise ValueError("No wikitable found on page. Wikipedia page structure may have changed.")

    # Use pandas to parse all tables; concatenate and keep common columns
    dfs = pd.read_html(str(soup), match="Flight No.")
    df = pd.concat(dfs, ignore_index=True)
    return df
