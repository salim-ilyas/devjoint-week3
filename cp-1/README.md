# Checkpoint 1 — Tool/Function Definitions

## Goal
Define 2–3 tools/functions the agent can call, each with a clear
**name**, **description**, and **parameter schema**. The description is
what the LLM reads to decide *when* to use a tool, so it has to be
specific enough to disambiguate from the other tools.

## What's here
`tools.py` defines three tools using Gemini's `FunctionDeclaration` /
`Tool` types from `google.generativeai.types`:

| Tool | Name | Purpose | Required params |
|---|---|---|---|
| Calculator | `calculator` | Basic arithmetic (add/subtract/multiply/divide) | `operand1`, `operand2`, `operator` |
| Weather | `get_weather` | Current weather for a city | `location` (optional: `unit`) |
| Search | `web_search` | Web lookup for current/factual info | `query` (optional: `num_results`) |

All three are bundled into a single `Tool` object (`agent_tools`) ready
to be passed to a `GenerativeModel(tools=...)` call in later checkpoints.

## Design notes
- **Calculator uses structured params**, not a raw expression string —
  avoids `eval()` on model-influenced input and makes it easier for the
  LLM to fill in correctly.
- **Weather's description explicitly mentions "where I am"** phrasing,
  since Checkpoint 4 requires a chained query like *"what's the weather
  where I am, then convert to Fahrenheit"*.
- **Search's description explicitly excludes math/weather** so the LLM
  doesn't default to search when a more specific tool applies.

## How to verify
```bash
pip install -r requirements.txt
python -c "from tools import agent_tools; print(agent_tools)"
```
This should print the three function declarations with no errors.

## Requirements
- `google-generativeai==0.8.6`

On Windows, make sure you install into the **active venv's**
interpreter, not a global Python:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```