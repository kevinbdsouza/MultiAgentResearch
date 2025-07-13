"""Example script for running the research agent."""
from multi_agent_research import BraveSearchClient, GeminiClient, ResearchAgent


def main() -> None:
    brave = BraveSearchClient()
    gemini = GeminiClient()
    agent = ResearchAgent(brave, gemini, num_subagents=2)
    query = "open source multi agent systems"
    summary = agent.run(query)
    print(summary)


if __name__ == "__main__":
    main()
