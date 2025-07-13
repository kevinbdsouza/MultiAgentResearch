import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from multi_agent_research.agent import ResearchAgent


class DummyBrave:
    def __init__(self):
        self.queries = []

    def search(self, query: str):
        self.queries.append(query)
        return [
            {"description": "result 1"},
            {"description": "result 2"},
        ]


class DummyGemini:
    def __init__(self):
        self.prompts = []

    def generate_content(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if "independent search tasks" in prompt:
            return "1. topic one\n2. topic two"
        return "summary"


def test_research_agent_sequence():
    brave = DummyBrave()
    gemini = DummyGemini()
    agent = ResearchAgent(brave, gemini, num_subagents=2)
    result = agent.run("test query")
    assert result == "summary"
    assert brave.queries == ["topic one", "topic two"]
    # first prompt for planning, second for summarization
    assert len(gemini.prompts) == 2
    assert "test query" in gemini.prompts[0]
