# This file contains a set of test cases for the get_tool_call function in agent_client.py.
from agent_client import get_tool_call

TEST_CASES = [
    # Calculator: different phrasings of the same operation
    {"message": "What's 45 times 12?", "expected_tool": "calculator"},
    {"message": "Add 15 and 27 for me", "expected_tool": "calculator"},
    {"message": "Can you divide 100 by 4?", "expected_tool": "calculator"},
    {"message": "8 minus 3", "expected_tool": "calculator"},

    # Weather: different phrasings
    {"message": "What's the weather in Baku right now?", "expected_tool": "get_weather"},
    {"message": "Is it raining in London today?", "expected_tool": "get_weather"},
    {"message": "How hot is it in Dubai?", "expected_tool": "get_weather"},

    # Search: different phrasings
    {"message": "Who won the last World Cup?", "expected_tool": "web_search"},
    {"message": "Search for the latest news about AI regulation", "expected_tool": "web_search"},
    {"message": "What's the current price of Bitcoin?", "expected_tool": "web_search"},

    # Negative cases: no tool should be called
    {"message": "Hello, how are you?", "expected_tool": None},
    {"message": "What is the capital of France?", "expected_tool": None},
    {"message": "Explain what a for-loop is.", "expected_tool": None},
]


def run_tests():
    passed = 0
    print(f"{'MESSAGE':<50} {'EXPECTED':<15} {'GOT':<15} RESULT")
    print("-" * 95)

    for case in TEST_CASES:
        tool_name, args = get_tool_call(case["message"])
        expected = case["expected_tool"]
        ok = tool_name == expected
        passed += ok

        print(
            f"{case['message']:<50} "
            f"{str(expected):<15} "
            f"{str(tool_name):<15} "
            f"{'PASS' if ok else 'FAIL'}"
        )
        if tool_name:
            print(f"    args: {args}")

    print("-" * 95)
    print(f"Result: {passed}/{len(TEST_CASES)} correct")


if __name__ == "__main__":
    run_tests()