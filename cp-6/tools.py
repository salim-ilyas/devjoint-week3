from google.generativeai.types import FunctionDeclaration, Tool

# calculator_tool is a FunctionDeclaration that defines a tool for performing basic arithmetic calculations. 
# it takes two operands and an operator as input parameters and returns the result of the calculation. 
# the tool is described in detail, including the types of operations it can perform (addition, subtraction, multiplication, division) and the required parameters.
calculator_tool = FunctionDeclaration(
    name="calculator",
    description=(
        """Perform a basic arithmetic calculation between two numbers.
        Use this whenever the user asks for a math result — addition, 
        subtraction, multiplication, or division — instead of computing 
        it yourself."""
    ),
    parameters={
        "type": "object",
        "properties": {
            "operand1": {
                "type": "number",
                "description": "The first number."
            },
            "operand2": {
                "type": "number",
                "description": "The second number."
            },
            "operator": {
                "type": "string",
                "description": "The arithmetic operation to be performed.",
                "enum": ["add", "subtract", "multiply", "divide"]
            }
        },
        "required": ["operand1", "operand2", "operator"]
    }
)

# weather_tool is a FunctionDeclaration that defines a tool for retrieving current weather conditions for a specific city.
# it takes a location (city name) and an optional unit (celsius or fahrenheit)
weather_tool = FunctionDeclaration(
    name="get_weather",
    description=(
        """Get the current weather conditions for a specific city. Use
        this when the user asks about temperature, conditions, or
        forecast for a location — including phrases like 'where I am'
        if a location has already been established in the conversation."""
    ),
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name like 'Baku' or 'London'."
            },
            "unit": {
                "type": "string",
                "description": "Temperature unit to return. Default is celsius.",
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["location"]
    }
)

# search_tool defines a tool for performing web searches to retrieve up-to-date information that the model may not know itself.
search_tool = FunctionDeclaration(
    name="web_search",
    description=(
        """Search the web for up-to-date or factual information the model
        would not reliably know on its own — current events, recent
        data, or anything requiring a fresh lookup. Do not use this for
        math or weather; use the calculator or get_weather tools instead."""
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query string."
            },
            "num_results": {
                "type": "integer",
                "description": "How many results to return. Defaults to 3."
            }
        },
        "required": ["query"]
    }
)

# agent tools defines a collection of tools that can be used by an agent to perform various tasks.
agent_tools = Tool(
    function_declarations=[calculator_tool, weather_tool, search_tool]
)