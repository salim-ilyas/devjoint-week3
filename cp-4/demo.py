# demo script for testing the agent with chained queries
from agent_client import run_agent

CHAINED_QUERIES = [
    # calculator -> weather
    "What's the weather in Baku, and what would double that temperature be?",

    # calculator -> search
    "What's 10 plus 5? Then search for what that number means as a famous football shirt number.",

    # single-tool control case, for comparison
    "What's the weather in London?",
]

if __name__ == "__main__":
    for query in CHAINED_QUERIES:
        print(f"\nUser: {query}")
        answer = run_agent(query)
        print(f"Agent: {answer}")