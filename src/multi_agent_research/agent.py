"""Research agent using a lead Gemini agent with search subagents."""
from __future__ import annotations

import asyncio
from typing import List

from .brave import BraveSearchClient
from .gemini import GeminiClient


class CitationAgent:
    """Agent that adds citations to the research report."""

    def __init__(self, gemini: GeminiClient):
        self.gemini = gemini

    def run(self, report: str, sources: List[dict]) -> str:
        """Add citations to the report."""
        prompt = (
            "You are a citation assistant. Your task is to add citations to the following research report "
            "based on the provided sources. For each claim in the report, find the most relevant source "
            "and add a citation in the format [#]. You should include the corresponding references at the bottom of the report. \n\n"
            f"Report:\n{report}\n\n"
            f"Sources:\n{sources}\n"
        )
        return self.gemini.generate_content(prompt)


class SearchSubAgent:
    """Subagent that performs a web search using Brave."""

    def __init__(self, brave: BraveSearchClient, gemini: GeminiClient):
        self.brave = brave
        self.gemini = gemini

    async def run(self, query: str) -> dict:
        """Execute the search and summarize the findings."""
        results = await asyncio.to_thread(self.brave.search, query)
        items = []
        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            desc = r.get("description", "")
            items.append(f"- {title} ({url}): {desc}")
        search_context = "\n".join(items)
        prompt = (
            "You are a research assistant. Your task is to summarize the following search results "
            f"for the query '{query}'. Focus on the most relevant information and "
            "extract key findings. Mention any useful URLs.\n\n"
            f"Search Results:\n{search_context}"
        )
        summary = await asyncio.to_thread(self.gemini.generate_content, prompt)
        return {"summary": summary, "sources": results}


class LeadAgent:
    """Orchestrator agent that plans and delegates tasks to sub-agents."""

    def __init__(self, gemini: GeminiClient, num_subagents: int = 3):
        self.gemini = gemini
        self.num_subagents = num_subagents
        self.memory = []

    def _add_to_memory(self, role: str, content: str):
        """Add a message to the agent's memory."""
        self.memory.append({"role": role, "content": content})

    def _plan_subqueries(self, query: str) -> List[str]:
        """Use Gemini to break the query into subqueries."""
        prompt = (
            "You are a research assistant. Your goal is to break down the following research question into "
            f"{self.num_subagents} independent search tasks. For each task, provide a concise search query. "
            "Return the queries as a numbered list. Don't return anything else in the numbered list apart from the queries. \n\n"
            f"Research Question: {query}"
        )
        plan = self.gemini.generate_content(prompt)
        self._add_to_memory("lead_agent", f"Plan: {plan}")
        subqueries = []
        for line in plan.splitlines():
            if "." in line:
                part = line.split(".", 1)[1].strip()
                if part:
                    subqueries.append(part)
        return subqueries[: self.num_subagents] or [query]

    async def _run_subagents(self, subqueries: List[str]) -> List[str]:
        """Run subagents in parallel."""
        tasks = [SearchSubAgent(BraveSearchClient(), self.gemini).run(q) for q in subqueries]
        return await asyncio.gather(*tasks)

    async def run(self, query: str) -> str:
        """Plan, delegate to subagents, and summarize results."""
        subqueries = self._plan_subqueries(query)
        self._add_to_memory("lead_agent", f"Subqueries: {subqueries}")
        results = await self._run_subagents(subqueries)
        self._add_to_memory("sub_agents", f"Results: {results}")

        summaries = [r["summary"] for r in results]
        sources = [r["sources"] for r in results]

        context = "\n\n".join(summaries)
        prompt = f"Summarize the following research findings for '{query}':\n{context}"
        summary = self.gemini.generate_content(prompt)
        self._add_to_memory("lead_agent", f"Summary: {summary}")

        citation_agent = CitationAgent(self.gemini)
        report_with_citations = citation_agent.run(summary, sources)
        self._add_to_memory("citation_agent", f"Report with citations: {report_with_citations}")

        return report_with_citations


class ResearchAgent:
    """Main class to run the multi-agent research system."""

    def __init__(self, brave: BraveSearchClient, gemini: GeminiClient, *, num_subagents: int = 3):
        self.brave = brave
        self.gemini = gemini
        self.lead_agent = LeadAgent(gemini, num_subagents)

    async def run(self, query: str) -> str:
        """Run the research process."""
        return await self.lead_agent.run(query)
