"""Brave search client."""
from __future__ import annotations

import os
from typing import List
import requests


class BraveSearchClient:
    """Simple wrapper around Brave search API."""

    BASE_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("BRAVE_SEARCH_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_SEARCH_API_KEY not provided")

    def search(self, query: str, count: int = 5) -> List[dict]:
        """Return a list of search result objects."""
        params = {"q": query, "count": count}
        headers = {"Accept": "application/json", "X-Subscription-Token": self.api_key}
        resp = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("web", {}).get("results", [])
        return results
