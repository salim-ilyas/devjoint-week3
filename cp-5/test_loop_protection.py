# Loop protection tests for the agent
from agent_client import run_agent

class FakeFunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args


class FakePart:
    def __init__(self, function_call=None):
        self.function_call = function_call


class FakeContent:
    def __init__(self, parts):
        self.parts = parts


class FakeCandidate:
    def __init__(self, parts):
        self.content = FakeContent(parts)


class FakeResponse:
    def __init__(self, parts, text=None):
        self.candidates = [FakeCandidate(parts)]
        self.text = text


# fake chat classes to simulate runaway vs normal model behavior

class RunawayChat:
# simulates a model that keeps calling tools without ever returning a final answer. Should hit the max_steps cap and stop safely.

    def __init__(self):
        self.send_message_calls = 0

    def send_message(self, _msg):
        self.send_message_calls += 1
        call = FakeFunctionCall(
            name="calculator",
            args={"operand1": 1, "operand2": 1, "operator": "add"},
        )
        return FakeResponse(parts=[FakePart(function_call=call)])


class NormalChat:
# simulates a model that calls a tool once and then returns a final answer. Should NOT hit the cap.

    def __init__(self):
        self.send_message_calls = 0

    def send_message(self, _msg):
        self.send_message_calls += 1
        if self.send_message_calls == 1:
            call = FakeFunctionCall(
                name="calculator",
                args={"operand1": 2, "operand2": 2, "operator": "add"},
            )
            return FakeResponse(parts=[FakePart(function_call=call)])
        return FakeResponse(parts=[FakePart(function_call=None)], text="2 + 2 is 4.")

def test_runaway_model_is_stopped_by_cap():
    chat = RunawayChat()
    max_steps = 5

    result = run_agent("simulate a runaway", max_steps=max_steps, chat=chat)

    assert "wasn't able to finish" in result, f"Expected safe stop message, got: {result}"
    # send_message is called once up front + once per step = max_steps + 1
    assert chat.send_message_calls == max_steps + 1, (
        f"Expected exactly {max_steps + 1} send_message calls, got {chat.send_message_calls}"
    )
    print(f"PASS: runaway model stopped after {max_steps} tool-call steps, no hang.")


def test_normal_model_does_not_hit_cap():
    chat = NormalChat()

    result = run_agent("what's 2 plus 2", max_steps=5, chat=chat)

    assert result == "2 + 2 is 4.", f"Expected final answer, got: {result}"
    assert chat.send_message_calls == 2, f"Expected 2 send_message calls, got {chat.send_message_calls}"
    print("PASS: normal single-tool flow returns final answer without hitting the cap.")


if __name__ == "__main__":
    test_runaway_model_is_stopped_by_cap()
    test_normal_model_does_not_hit_cap()
    print("\nAll loop-protection tests passed.")