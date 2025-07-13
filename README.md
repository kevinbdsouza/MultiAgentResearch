# Multi Agent Research

This project provides a sequential multi-agent web research system that uses
Brave Search to gather information and Gemini to summarize the results.

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
