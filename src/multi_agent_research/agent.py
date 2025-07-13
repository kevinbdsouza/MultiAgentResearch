"""Research agent that uses Brave search and Gemini."""
from __future__ import annotations

from typing import List

from .brave import BraveSearchClient
from .gemini import GeminiClient


class ResearchAgent:
    """Simple sequential research agent."""

    def __init__(self, brave: BraveSearchClient, gemini: GeminiClient):
        self.brave = brave
        self.gemini = gemini

    def run(self, query: str) -> str:
        """Search the web and summarize results."""
        results = self.brave.search(query)
        snippets = "\n".join(r.get("description", "") for r in results)
        prompt = f"Summarize the following search results for the query '{query}':\n{snippets}"
        summary = self.gemini.generate_content(prompt)
        return summary
