import requests
from typing import Any, Callable, Self
from tools import call_tool
import re
import json
from logs import debug

URL: str = "http://localhost:11434/api/chat"
MODEL_NAME: str = "phi3"

class ChatHistory:
    SYS_ROLE: str = "system"
    LLM_ROLE: str = "assistant"
    USER_ROLE: str = "user"
    TOOL_ROLE: str = "tool"

    def __init__(self) -> None:
        self.messages: list[dict] = []
    
    def __append_message(self, role: str, content: str) -> Self:
        self.messages.append({
            "role": role,
            "content": content
        })
        return self
    
    def sys_message(self, content: str) -> Self:
        return self.__append_message(ChatHistory.SYS_ROLE, content)
    
    def user_message(self, content: str) -> Self:
        return self.__append_message(ChatHistory.USER_ROLE, content)
    
    def tool_message(self, content: str) -> Self:
        return self.__append_message(ChatHistory.TOOL_ROLE, content)
    
    def ai_message(self, content: str) -> Self:
        return self.__append_message(ChatHistory.LLM_ROLE, content)

def chat_request(history: ChatHistory) -> str:
    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": history.messages,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    response = requests.post(URL, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]

def extract_json(text: str) -> dict | None:
    json_re: str = r"\{.*tool.*arguments.*\}"
    match: re.Match | None = re.search(json_re, text, re.DOTALL)
    
    result: dict | None = None
    if match:
        try:
            result = json.loads(match.group())
        except Exception:
            pass
    
    return result

def process_LLM(history: ChatHistory) -> str:
    reply: str = chat_request(history)
    tool_data: dict | None = extract_json(reply)
    if tool_data:
        debug(f"TOOL CALL = {tool_data}")
        tool_response: str = call_tool(tool_data)
        debug(f"TOOL RESPONSE = {tool_response}")
        if tool_response:
            history.tool_message(json.dumps({"weather": tool_response}))
            reply = tool_response
    history.ai_message(reply)

    return reply

def cycle_LLM(history: ChatHistory) -> str:
    turn, max_turns = 0, 10
    while turn < max_turns:
        reply: str = chat_request(history)
        tool_data: dict | None = extract_json(reply)
        if tool_data is None:
            break
        else:
            turn += 1
            debug(f"TOOL CALL #{turn} with the tool {tool_data}")
            tool_response: str = call_tool(tool_data)
            debug(f"TOOL RESPONSE = {tool_response}")
            if tool_response:
                history.tool_message(json.dumps({"weather": tool_response}))
                
    history.ai_message(reply)

    return reply
