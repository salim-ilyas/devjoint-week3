import os
from dotenv import load_dotenv
import google.generativeai as genai
from tools import agent_tools

load_dotenv()  # reads the API key from the local .env file

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


def get_tool_call(user_message: str):
    # this function simply takes a user message and returns the name of the tool and the arguments to pass to that tool, if any.
    response = model.generate_content(user_message)

    candidate = response.candidates[0]
    for part in candidate.content.parts:
        if part.function_call and part.function_call.name:
            fn = part.function_call
            return fn.name, dict(fn.args)

    return None, None