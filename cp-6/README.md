# Checkpoint 6 — Clear Reasoning/Tool-Call Trace Logging

## Goal
Make the agent's decision-making visible for debugging: what it decided
to do at each step, which tool it called with what arguments, what that
tool returned, and why it stopped when it did.

## What's here
`agent_client.py` replaces the `print()` calls from earlier checkpoints
with Python's `logging` module:
- every line is timestamped and leveled (`INFO` for normal steps,
  `WARNING` for the loop-limit stop or an unknown tool)
- output goes to **both** the console and `agent_trace.log`, so a
  session's full trace survives after the terminal scrolls away
- each line states the *decision* being made, not just raw data —
  e.g. `DECISION (step 2/5): call tool 'calculator' with args=...`
  rather than just dumping the args

`trace_demo.py` — runs a **mocked** chained query (weather → calculator
→ final answer) without needing a live API key, so the log format can
be verified deterministically.

`demo.py` — the live-API version, same idea but hits the real model.

## Verified output (from trace_demo.py, actually run)

```
2026-08-06 19:02:04 | INFO    | USER REQUEST: "What's the weather in Baku, and double that temperature?"
2026-08-06 19:02:04 | INFO    | DECISION (step 1/5): call tool 'get_weather' with args={'location': 'Baku'}
2026-08-06 19:02:04 | INFO    | TOOL RESULT (step 1): get_weather -> {'location': 'Baku', 'condition': 'sunny', 'temperature': 32, 'unit': 'celsius'}
2026-08-06 19:02:04 | INFO    | DECISION (step 2/5): call tool 'calculator' with args={'operand1': 32, 'operand2': 2, 'operator': 'multiply'}
2026-08-06 19:02:04 | INFO    | TOOL RESULT (step 2): calculator -> 64
2026-08-06 19:02:04 | INFO    | DECISION (step 3): no tool needed, answering directly
2026-08-06 19:02:04 | INFO    | FINAL RESPONSE: "It's 32°C in Baku, and double that is 64."
```

Same content was also confirmed written to `agent_trace.log`, not just
the console.

## Setup & Run
```bash
pip install -r requirements.txt
python trace_demo.py          # no API key needed
cp .env.example .env           # then paste your real key
python demo.py                 # live version
```

## Live results

> Paste your `demo.py` output here after running it with your key.

```
(paste output here)
```

## Requirements
- `google-generativeai==0.8.6`
- `python-dotenv`

Note: `agent_trace.log` is git-ignored (see `.gitignore`) since it's a
runtime debug artifact, not source — regenerated fresh each run.