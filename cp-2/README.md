# Checkpoint 2 — Right Tool Selection

## Goal
Show the agent picks the correct tool based on the user's request,
tested across **different phrasings** of the same intent — not just one
fixed sentence per tool.

## What's here
- `tools.py` — same 3 tool definitions from Checkpoint 1
- `agent_client.py` — configures `GenerativeModel` with the tools and
  exposes `get_tool_call(message)`, which returns `(tool_name, args)`,
  or `(None, None)` if the model chose to answer directly
- `test_tool_selection.py` — 13 test cases:
  - 4 phrasings that should trigger `calculator`
  - 3 phrasings that should trigger `get_weather`
  - 3 phrasings that should trigger `web_search`
  - 3 **negative cases** that should trigger no tool at all (greetings,
    general knowledge, code explanation)

## Why the negative cases matter
An agent that reaches for a tool on every message isn't actually doing
"selection" — it's just always calling something. Testing that plain
factual/conversational questions get answered directly (no tool call)
is as important as testing that math/weather/search questions route
correctly.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# then edit .env and paste your real GOOGLE_API_KEY
```

## Run
```bash
python test_tool_selection.py
```

## Results

> Fill this in after running it — paste the actual pass/fail table and
> final score here. If anything fails, note which phrasing tripped it
> up and whether it was a tool-description wording issue (fix in
> `tools.py`) or a genuine model limitation.

```
(paste output here)
```

## Requirements
- `google-generativeai==0.8.6`
- `python-dotenv` — loads `GOOGLE_API_KEY` from `.env`, which is
  git-ignored so the key is never committed