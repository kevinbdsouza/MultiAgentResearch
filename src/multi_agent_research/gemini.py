"""Gemini API client."""
from __future__ import annotations

import os
import requests


class GeminiClient:
    """Wrapper around Gemini text generation API."""

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided")

    def generate_content(self, prompt: str) -> str:
        """Generate content from Gemini API."""
        params = {"key": self.api_key}
        headers = {"Content-Type": "application/json"}
        body = {"contents": [{"parts": [{"text": prompt}]}]}
        resp = requests.post(self.BASE_URL, params=params, json=body, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
