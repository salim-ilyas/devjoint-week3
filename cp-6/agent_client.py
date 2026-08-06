import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from tools import agent_tools
from tool_functions import TOOL_FUNCTIONS

load_dotenv()

logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("agent_trace.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

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

MAX_TOOL_STEPS = int(os.environ.get("AGENT_MAX_TOOL_STEPS", "5"))


def run_agent(user_message: str, max_steps: int = None, chat=None) -> str:
    if max_steps is None:
        max_steps = MAX_TOOL_STEPS
    if chat is None:
        chat = model.start_chat()

    logger.info(f"USER REQUEST: {user_message!r}")
    response = chat.send_message(user_message)

    for step in range(1, max_steps + 1):
        part = response.candidates[0].content.parts[0]

        if not part.function_call or not part.function_call.name:
            logger.info(f"DECISION (step {step}): no tool needed, answering directly")
            logger.info(f"FINAL RESPONSE: {response.text!r}")
            return response.text

        tool_name = part.function_call.name
        args = dict(part.function_call.args)
        logger.info(
            f"DECISION (step {step}/{max_steps}): call tool '{tool_name}' "
            f"with args={args}"
        )

        if tool_name not in TOOL_FUNCTIONS:
            logger.warning(f"UNKNOWN TOOL requested: '{tool_name}' — stopping")
            return f"I tried to use a tool I don't recognize ('{tool_name}')."

        result = TOOL_FUNCTIONS[tool_name](**args)
        logger.info(f"TOOL RESULT (step {step}): {tool_name} -> {result!r}")

        function_response = genai.protos.Part(
            function_response=genai.protos.FunctionResponse(
                name=tool_name,
                response={"result": result},
            )
        )
        response = chat.send_message(genai.protos.Content(parts=[function_response]))

    logger.warning(
        f"LOOP LIMIT HIT: reached max_steps={max_steps} without a final answer "
        f"— stopping to avoid an infinite loop"
    )
    return (
        f"I wasn't able to finish this request within {max_steps} tool calls, "
        f"so I'm stopping here to avoid looping indefinitely. Could you "
        f"rephrase or simplify the request?"
    )