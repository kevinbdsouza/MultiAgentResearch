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

Set the following environment variables with your API keys:

- `BRAVE_SEARCH_API_KEY`
- `GEMINI_API_KEY`

## Usage

Run the example script:

```bash
python examples/run_research.py
```

## Testing

```bash
pytest
```
