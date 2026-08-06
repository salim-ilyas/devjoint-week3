# demo script for running the agent with a few example queries

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


class ChainedFakeChat:
# simulates a model that calls one tool, then another, and finally returns a final answer. Should NOT hit the cap.
    def __init__(self):
        self.calls = 0

    def send_message(self, _msg):
        self.calls += 1
        if self.calls == 1:
            call = FakeFunctionCall(name="get_weather", args={"location": "Baku"})
            return FakeResponse(parts=[FakePart(function_call=call)])
        if self.calls == 2:
            call = FakeFunctionCall(
                name="calculator",
                args={"operand1": 32, "operand2": 2, "operator": "multiply"},
            )
            return FakeResponse(parts=[FakePart(function_call=call)])
        return FakeResponse(
            parts=[FakePart(function_call=None)],
            text="It's 32°C in Baku, and double that is 64.",
        )


if __name__ == "__main__":
    fake_chat = ChainedFakeChat()
    answer = run_agent(
        "What's the weather in Baku, and double that temperature?",
        chat=fake_chat,
    )
    print(f"\nFinal answer returned to user: {answer}")