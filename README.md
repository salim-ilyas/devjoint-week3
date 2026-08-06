# Week 3 — AI Agent with Tool/Function Calling

An agent built on Google's Gemini API (`gemini-1.5-flash`) that can
call tools, chain multiple tool calls together when a request needs
it, protect itself against infinite loops, and log its own reasoning
for debugging. Built incrementally across 6 checkpoints, each in its
own self-contained folder.

## Folder structure

```
checkpoint-1/   Tool/function definitions
checkpoint-2/   Right tool selection (tested across phrasings)
checkpoint-3/   Tool execution + natural-language final response
checkpoint-4/   Chained tool usage (2 tools in a row)
checkpoint-5/   Infinite-loop / max-retry protection
checkpoint-6/   Reasoning & tool-call trace logging
```

Each folder is self-contained: its own `tools.py`, its own
`requirements.txt`, its own `README.md` with that checkpoint's specific
goal, design notes, and results. `checkpoint-6/` holds the final,
most complete version of the agent (`agent_client.py` there is the
cumulative result of all 6 checkpoints' work).

## Checkpoints at a glance

| # | Checkpoint | Points | Folder |
|---|---|---|---|
| 1 | Tool/function definitions (name, description, params) | 15 | `checkpoint-1/` |
| 2 | Right tool selection across varied phrasings | 25 | `checkpoint-2/` |
| 3 | Tool execution + final natural-language response | 20 | `checkpoint-3/` |
| 4 | Chained tool usage (2 tools in sequence) | 20 | `checkpoint-4/` |
| 5 | Infinite-loop / max-retry protection | 15 | `checkpoint-5/` |
| 6 | Reasoning/tool-call trace logging | 5 | `checkpoint-6/` |

## The 3 tools

| Tool | Name | What it does |
|---|---|---|
| Calculator | `calculator` | Real arithmetic (add/subtract/multiply/divide) |
| Weather | `get_weather` | Mocked weather lookup (no external API key needed) |
| Search | `web_search` | Mocked web search results (no external API key needed) |

Weather and search are intentionally mocked so the whole project runs
without needing extra third-party API keys beyond Gemini's — the
checkpoints are graded on the *agent mechanics* (selection, execution,
chaining, loop safety, logging), not on live data accuracy. Either can
be swapped for a real API later without changing function signatures.

## Setup (once, applies to every checkpoint folder)

```bash
python -m venv venv
.\venv\Scripts\activate          # Windows
pip install -r requirements.txt  # inside whichever checkpoint folder you're running
```

Create a `.env` file (copy from `.env.example`) with:
```
GOOGLE_API_KEY=your_gemini_api_key_here
AGENT_MAX_TOOL_STEPS=5
```

**Never commit `.env`** — it's git-ignored. Only `.env.example` (a
template with no real key) is tracked.

## Running each checkpoint

Most checkpoints have a `demo.py` (live, needs your API key) — some
also have a `trace_demo.py` or `test_*.py` that runs without one,
using a mocked model, for deterministic testing (Checkpoints 5 and 6).

```bash
cd checkpoint-N
python demo.py
```