from chat_request import ChatLLM
from logs import debug
from extract_json import extract_json
from tools import call_tool
import json

def process_LLM(chat: ChatLLM) -> str:
    reply: str = chat.request()
    tool_data: dict | None = extract_json(reply, ["tool", "arguments"])
    if tool_data:
        debug(f"TOOL CALL = {tool_data}")
        tool_response: str = call_tool(tool_data)
        debug(f"TOOL RESPONSE = {tool_response}")
        if tool_response:
            chat.tool_message(json.dumps({"weather": tool_response}))
            reply = tool_response
    chat.ai_message(reply)

    return reply