from typing import Callable
from travel_info import travel_info

TOOLS: dict[str, Callable] = {
    "travel_info": travel_info
}

def call_tool(tool_data: dict) -> str:
    result: str = ""
    callable: Callable | None = TOOLS.get(tool_data.get("tool", ""))
    if callable:
        arguments: dict = tool_data.get("arguments", {})
        result = callable(**arguments)
    
    return result
