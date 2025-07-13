"""Research agent using a lead Gemini agent with search subagents."""
from __future__ import annotations

from typing import List

from .brave import BraveSearchClient
from .gemini import GeminiClient


class SearchSubAgent:
    """Subagent that performs a web search using Brave."""

    def __init__(self, brave: BraveSearchClient):
        self.brave = brave

    def run(self, query: str) -> list[dict]:
        """Execute the search and return the raw results."""
        return self.brave.search(query)


class ResearchAgent:
    """Lead agent that coordinates search subagents."""

    def __init__(self, brave: BraveSearchClient, gemini: GeminiClient, *, num_subagents: int = 3):
        self.brave = brave
        self.gemini = gemini
        self.num_subagents = num_subagents

    # Planning -----------------------------------------------------------------
    def _plan_subqueries(self, query: str) -> List[str]:
        """Use Gemini to break the query into subqueries."""
        prompt = (
            "Break the following research question into "
            f"{self.num_subagents} independent search tasks. "
            "Return them as a numbered list.\n" + query
        )
        plan = self.gemini.generate_content(prompt)
        subqueries = []
        for line in plan.splitlines():
            if "." in line:
                part = line.split(".", 1)[1].strip()
                if part:
                    subqueries.append(part)
        return subqueries[: self.num_subagents] or [query]

    # Execution ----------------------------------------------------------------
    def _run_subagent(self, subquery: str) -> str:
        agent = SearchSubAgent(self.brave)
        results = agent.run(subquery)
        snippets = "\n".join(r.get("description", "") for r in results)
        return f"Results for '{subquery}':\n{snippets}"

    def run(self, query: str) -> str:
        """Plan, delegate to subagents, and summarize results."""
        subqueries = self._plan_subqueries(query)
        findings = [self._run_subagent(q) for q in subqueries]
        context = "\n\n".join(findings)
        prompt = f"Summarize the following research findings for '{query}':\n{context}"
        return self.gemini.generate_content(prompt)
