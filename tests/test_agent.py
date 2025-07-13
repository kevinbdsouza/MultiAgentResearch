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
        return "summary"


def test_research_agent_sequence():
    brave = DummyBrave()
    gemini = DummyGemini()
    agent = ResearchAgent(brave, gemini)
    result = agent.run("test query")
    assert result == "summary"
    assert brave.queries == ["test query"]
    assert len(gemini.prompts) == 1
    assert "test query" in gemini.prompts[0]
