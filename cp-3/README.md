# Checkpoint 3 — Tool Execution + Final Natural-Language Response

## Goal
When the model picks a tool, actually **execute** it in Python, send the
real result back to the model, and get a final natural-language answer
— not just print the raw function-call JSON.

## What's here
- `tools.py` — tool declarations (from Checkpoint 1)
- `tool_functions.py` — the real implementations:
  - `calculator()` — genuine arithmetic
  - `get_weather()` — **mocked** (small lookup table for Baku/London/Dubai,
    falls back to a generic "unknown" reading for other cities). No API
    key required. Can be swapped for a real weather API later without
    changing its signature.
  - `web_search()` — **mocked** placeholder results, same reasoning.
- `agent_client.py` — `run_agent(user_message)` does the full round trip:
  1. send message → model picks a tool (or not)
  2. if a tool was picked, run the matching Python function
  3. send the tool's actual result back to the model via `chat.send_message()`
  4. return the model's final natural-language response
- `demo.py` — runs 4 example queries end-to-end and prints the final
  natural-language answers

## Why mocked weather/search
The checkpoint is graded on the **execution + round-trip mechanism**,
not on live data accuracy. Mocking keeps the demo runnable with zero
extra API keys, while still proving the full loop: tool call → real
Python execution → result fed back → natural language response.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# paste your GOOGLE_API_KEY into .env
```

## Run
```bash
python demo.py
```

## Results

> Paste actual output here after running, e.g.:
> ```
> User: What's 45 times 12?
>   -> model chose tool: calculator({'operand1': 45.0, 'operand2': 12.0, 'operator': 'multiply'})
>   -> tool result: 540.0
> Agent: 45 times 12 is 540.
> ```

## Requirements
- `google-generativeai==0.8.6`
- `python-dotenv`