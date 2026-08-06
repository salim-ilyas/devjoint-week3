# tool functions that the model can call. Each function should take a dict of arguments and return a dict of results.
def calculator(operand1: float, operand2: float, operator: str) -> float:
    if operator == "add":
        return operand1 + operand2
    if operator == "subtract":
        return operand1 - operand2
    if operator == "multiply":
        return operand1 * operand2
    if operator == "divide":
        if operand2 == 0:
            raise ValueError("Cannot divide by zero.")
        return operand1 / operand2
    raise ValueError(f"Unknown operator: {operator}")


# small mocked weather table so results are deterministic for grading/demo.
_MOCK_WEATHER = {
    "baku": {"condition": "sunny", "temp_c": 32},
    "london": {"condition": "rainy", "temp_c": 16},
    "dubai": {"condition": "clear", "temp_c": 41},
}


def get_weather(location: str, unit: str = "celsius") -> dict:
    key = location.strip().lower()
    data = _MOCK_WEATHER.get(key, {"condition": "unknown", "temp_c": 20})
    temp_c = data["temp_c"]

    if unit == "fahrenheit":
        temp = temp_c * 9 / 5 + 32
    else:
        temp = temp_c

    return {
        "location": location,
        "condition": data["condition"],
        "temperature": round(temp, 1),
        "unit": unit,
    }


def web_search(query: str, num_results: int = 3) -> list:
    # mocked results — swap with a real search API call here.
    return [
        {
            "title": f"Mock result {i + 1} for '{query}'",
            "snippet": f"This is a placeholder search result about '{query}'.",
        }
        for i in range(num_results)
    ]


# dispatch table: maps the tool "name" the model calls -> the function to run.
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_weather": get_weather,
    "web_search": web_search,
}