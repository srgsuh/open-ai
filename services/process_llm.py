import json
from logs import debug
from services.chat_request import ChatLLM
from services.extract_json import extract_json
from services.tools import call_tool

def process_LLM(chat: ChatLLM) -> str:
    reply: str = chat.request()
    tool_data: dict | None = extract_json(reply, ["tool", "arguments"])
    if tool_data:
        debug(f"TOOL CALL = {tool_data}")
        tool_response: str = call_tool(tool_data)
        debug(f"TOOL RESPONSE = {tool_response}")
        if tool_response:
            chat.tool_message(json.dumps({"response": tool_response}))
            reply = tool_response
    chat.ai_message(reply)

    return reply