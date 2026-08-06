# Checkpoint 4 — Chained Tool Usage

## Goal
Handle queries that need **two tools in a row**, where the second tool's
input depends on the first tool's output — e.g. "what's the weather
where I am, then convert it to Fahrenheit."

## What's here
`agent_client.py` turns Checkpoint 3's single round trip into a **loop**:
after sending a tool's result back to the model, it checks whether the
model wants to call *another* tool before answering, and keeps going
until the model gives a final natural-language answer (or `max_steps`
is hit).

`demo.py` has 3 test queries:
1. **Weather → Calculator**: get the temperature, then do math on it
2. **Calculator → Search**: compute a number, then look it up
3. **Single-tool control case**: confirms the loop doesn't force a
   second tool call when only one is actually needed

## Why query #1 is phrased the way it is
`get_weather` already accepts a `unit` param internally, so a query like
"what's the weather in Baku in Fahrenheit" could resolve in **one** tool
call, not two — that wouldn't actually test chaining. Query #1 instead
asks for a **calculation on the returned number** ("double that
temperature"), which the weather tool has no way to do itself, forcing
a genuine two-tool sequence: `get_weather` → `calculator`.

## Important scope note
`max_steps=5` in `agent_client.py` is a **practical safety net**, not
the deliverable for infinite-loop protection — that's Checkpoint 5's
job, which adds proper configuration, logging of *why* a limit was
hit, and tests against runaway scenarios.

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

> Paste actual output here after running — confirm each query in the
> "Step 1 / Step 2" printout actually shows TWO different tools firing
> for queries 1 and 2, and only ONE for query 3.

```
(paste output here)
```

## Requirements
- `google-generativeai==0.8.6`
- `python-dotenv`