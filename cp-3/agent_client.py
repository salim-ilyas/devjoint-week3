# It uses the Google Generative AI API to run a chat model that can call tools to answer user queries.
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


def run_agent(user_message: str) -> str:
    chat = model.start_chat()
    response = chat.send_message(user_message)

    # look for a function call in the model's first response.
    part = response.candidates[0].content.parts[0]

    if not part.function_call or not part.function_call.name:
        # no tool needed — the model answered directly.
        return response.text

    tool_name = part.function_call.name
    args = dict(part.function_call.args)

    print(f"  -> model chose tool: {tool_name}({args})")

    if tool_name not in TOOL_FUNCTIONS:
        return f"Error: model requested unknown tool '{tool_name}'"

    result = TOOL_FUNCTIONS[tool_name](**args)
    print(f"  -> tool result: {result}")

    # send the tool's result back so the model can phrase a final answer.
    function_response = genai.protos.Part(
        function_response=genai.protos.FunctionResponse(
            name=tool_name,
            response={"result": result},
        )
    )
    final_response = chat.send_message(
        genai.protos.Content(parts=[function_response])
    )

    return final_response.text