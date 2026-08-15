# Demo script for running the agent with a few example queries
from agent_client import run_agent

QUERIES = [
    "What's 45 times 12?",
    "What's the weather in Baku, and what would double that temperature be?",
    "What is the capital of France?",
]

if __name__ == "__main__":
    for q in QUERIES:
        print(f"\n--- User: {q} ---")
        answer = run_agent(q)
        print(f"Agent: {answer}")