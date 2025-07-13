import pytest
import asyncio
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from multi_agent_research.agent import ResearchAgent


class DummyBrave:
    def __init__(self):
        self.queries = []

    def search(self, query: str):
        self.queries.append(query)
        return [
            {"description": "result 1", "url": "https://example.com/result1"},
            {"description": "result 2", "url": "https://example.com/result2"},
        ]


class DummyGemini:
    def __init__(self):
        self.prompts = []

    def generate_content(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if "independent search tasks" in prompt:
            return "1. topic one\n2. topic two"
        if "citation assistant" in prompt:
            return "report with citations"
        return "summary"


@pytest.mark.asyncio
async def test_research_agent_sequence():
    brave = DummyBrave()
    gemini = DummyGemini()
    agent = ResearchAgent(brave, gemini, num_subagents=2)

    # Mock the BraveSearchClient to avoid the API key error
    from unittest.mock import patch
    with patch('multi_agent_research.agent.BraveSearchClient', return_value=brave):
        result = await agent.run("test query")

    assert result == "report with citations"
    assert brave.queries == ["topic one", "topic two"]
    # planning + 2 subagent summaries + final summary + citation
    assert len(gemini.prompts) == 5
    assert "test query" in gemini.prompts[0]
    assert "citation assistant" in gemini.prompts[4]
