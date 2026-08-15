import os
from dotenv import load_dotenv
import google.generativeai as genai
from tools import agent_tools
from tool_functions import TOOL_FUNCTIONS

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError(
        "GOOGLE_API_KEY not found. Create a .env file with:\n"
        "GOOGLE_API_KEY=your_key_here"
    )

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-3.5-flash",
    tools=[agent_tools],
)

# configurable max tool-call steps per request. Defaults to 5 if unset.
MAX_TOOL_STEPS = int(os.environ.get("AGENT_MAX_TOOL_STEPS", "5"))


def run_agent(user_message: str, max_steps: int = None, chat=None) -> str:
    # run_agent is the main entry point for the agent. It takes a user message, sends it to the model, and handles any tool calls the model makes. It returns the final answer from the model.
    if max_steps is None:
        max_steps = MAX_TOOL_STEPS
    if chat is None:
        chat = model.start_chat()

    response = chat.send_message(user_message)

    for step in range(1, max_steps + 1):
        part = response.candidates[0].content.parts[0]

        if not part.function_call or not part.function_call.name:
            return response.text

        tool_name = part.function_call.name
        args = dict(part.function_call.args)
        print(f"  [step {step}/{max_steps}] tool call: {tool_name}({args})")

        if tool_name not in TOOL_FUNCTIONS:
            print(f"  [step {step}] ERROR: unknown tool '{tool_name}'")
            return f"I tried to use a tool I don't recognize ('{tool_name}')."

        result = TOOL_FUNCTIONS[tool_name](**args)
        print(f"  [step {step}] tool result: {result}")

        function_response = genai.protos.Part(
            function_response=genai.protos.FunctionResponse(
                name=tool_name,
                response={"result": result},
            )
        )
        response = chat.send_message(genai.protos.Content(parts=[function_response]))

    # loop protection: we've hit max_steps without a final answer.
    print(
        f"  [WARNING] Reached max_steps={max_steps} without a final answer. "
        f"Stopping to avoid an infinite loop."
    )
    return (
        f"I wasn't able to finish this request within {max_steps} tool calls, "
        f"so I'm stopping here to avoid looping indefinitely. Could you "
        f"rephrase or simplify the request?"
    )