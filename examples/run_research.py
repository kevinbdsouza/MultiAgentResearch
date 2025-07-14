"""Example script for running the research agent."""
import asyncio
import os
from dotenv import load_dotenv

from multi_agent_research import BraveSearchClient, GeminiClient, ResearchAgent


async def main() -> None:
    # Load environment variables from .env file
    load_dotenv()

    # Initialize clients with API keys
    brave = BraveSearchClient()
    gemini = GeminiClient()
    agent = ResearchAgent(brave, gemini, num_subagents=2)
    query = "open source multi agent systems"
    summary = await agent.run(query)
    print(summary)


if __name__ == "__main__":
    asyncio.run(main())
