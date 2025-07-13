# Multi Agent Research

This project provides a simple multi-agent web research system. A lead Gemini
agent decomposes the user query into subqueries, spawns Brave-powered search
subagents, and then summarizes their findings.

## Setup

Use [`uv`](https://github.com/astral-sh/uv) for isolated Python environments and
dependency management:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e .[dev]
```

Create a `.env` file and set your API keys:

```bash
BRAVE_SEARCH_API_KEY=your_brave_key
GEMINI_API_KEY=your_gemini_key
```

## Usage

Run the example script:

```bash
python examples/run_research.py
```

## Testing

```bash
pytest
```
