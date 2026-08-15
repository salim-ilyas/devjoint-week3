# this is a simple demo script that shows how to use the agent client to run queries and get answers from the agent.
from agent_client import run_agent

DEMO_QUERIES = [
    "What's 45 times 12?",
    "What's the weather in Baku?",
    "Search for the latest news about AI regulation",
    "What is the capital of France?",  # no tool expected
]

if __name__ == "__main__":
    for query in DEMO_QUERIES:
        print(f"\nUser: {query}")
        answer = run_agent(query)
        print(f"Agent: {answer}")