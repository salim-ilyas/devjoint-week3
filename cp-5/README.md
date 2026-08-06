# Checkpoint 5 — Protection Against Infinite Loops

## Goal
Make sure the agent can't loop forever calling tools — a hard maximum
retry/step limit that always terminates with a safe response.

## What's here
`agent_client.py` hardens Checkpoint 4's loop:
- `MAX_TOOL_STEPS` is a named constant, configurable via the
  `AGENT_MAX_TOOL_STEPS` environment variable (defaults to 5)
- every step is logged: `[step N/max] tool call: ...`
- if the cap is hit, it's logged as a clear `[WARNING]`, and the
  function returns a safe, user-facing message instead of hanging,
  crashing, or silently returning nothing
- `chat` is now an injectable parameter, so the loop can be tested
  with a **fake, deliberately-runaway chat object** instead of relying
  on the real model to misbehave on command (it won't reliably do
  that — this is the only way to test this deterministically)

`test_loop_protection.py` — two tests, no live API calls:
1. **`test_runaway_model_is_stopped_by_cap`** — a fake chat that
   *always* returns another tool call, forever. Confirms the agent
   stops at exactly `max_steps` and returns the safe message instead
   of looping indefinitely.
2. **`test_normal_model_does_not_hit_cap`** — a fake chat that calls
   one tool then answers normally. Confirms the cap doesn't interfere
   with ordinary, well-behaved flows.

## Why mocked, not live
A well-behaved model won't reliably loop forever just because you ask
it to, so there's no reliable live prompt that proves the safety net
actually works. Mocking the chat object lets us simulate the exact
failure mode we're protecting against and prove the fix deterministically.

## Setup & Run
```bash
pip install -r requirements.txt
python test_loop_protection.py
```

## Results (actual, verified)

```
  [step 1/5] tool call: calculator({'operand1': 1, 'operand2': 1, 'operator': 'add'})
  [step 1] tool result: 2
  [step 2/5] tool call: calculator({'operand1': 1, 'operand2': 1, 'operator': 'add'})
  [step 2] tool result: 2
  [step 3/5] tool call: calculator({'operand1': 1, 'operand2': 1, 'operator': 'add'})
  [step 3] tool result: 2
  [step 4/5] tool call: calculator({'operand1': 1, 'operand2': 1, 'operator': 'add'})
  [step 4] tool result: 2
  [step 5/5] tool call: calculator({'operand1': 1, 'operand2': 1, 'operator': 'add'})
  [step 5] tool result: 2
  [WARNING] Reached max_steps=5 without a final answer. Stopping to avoid an infinite loop.
PASS: runaway model stopped after 5 tool-call steps, no hang.
  [step 1/5] tool call: calculator({'operand1': 2, 'operand2': 2, 'operator': 'add'})
  [step 1] tool result: 4
PASS: normal single-tool flow returns final answer without hitting the cap.

All loop-protection tests passed.
```

Both tests pass: the runaway simulation is stopped exactly at the
5-step cap with a safe message, and normal single-tool flows are
unaffected by the cap.

## Requirements
- `google-generativeai==0.8.6`
- `python-dotenv`