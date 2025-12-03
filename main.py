import requests
from typing import Any, Callable
from tools import TOOLS
from system_content import SYSTEM_CONTENT
import re
import json
from thinking_dots import start_thinking_dots
import threading
from logs import debug

SYS_ROLE: str = "system"
LLM_ROLE: str = "assistant"
USER_ROLE: str = "user"
TOOL_ROLE: str = "tool"

URL: str = "http://localhost:11434/api/chat"
MODEL_NAME: str = "phi3"

def chat_request(messages: list) -> str:
    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": messages,
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

def call_tool(tool_data: dict) -> str:
    result: str = ""
    callable: Callable | None = TOOLS.get(tool_data.get("tool", ""))
    if callable:
        arguments: dict = tool_data.get("arguments", {})
        result = callable(**arguments)
    
    return result

def process_LLM(messages: list) -> str:
    reply: str = chat_request(messages)
    tool_data: dict | None = extract_json(reply)
    if tool_data:
        debug(f"TOOL CALL = {tool_data}")
        tool_response: str = call_tool(tool_data)
        debug(f"TOOL RESPONSE = {tool_response}")
        if tool_response:
            messages.append({
                "role": "tool",
                "content": json.dumps({"weather": tool_response})
            })
            reply = tool_response
    messages.append({"role": LLM_ROLE, "content": reply})

    return reply

def cycle_LLM(messages: list) -> str:
    turn, max_turns = 0, 10
    while turn < max_turns:
        reply: str = chat_request(messages)
        tool_data: dict | None = extract_json(reply)
        if tool_data is None:
            break
        else:
            turn += 1
            debug(f"TOOL CALL #{turn} with the tool {tool_data}")
            tool_response: str = call_tool(tool_data)
            debug(f"TOOL RESPONSE = {tool_response}")
            if tool_response:
                messages.append({
                    "role": TOOL_ROLE,
                    "content": json.dumps({"weather": tool_response})
                })
    messages.append({"role": LLM_ROLE, "content": reply})

    return reply


if __name__ == "__main__":
    debug("Start")
    messages = [{"role": SYS_ROLE, "content": SYSTEM_CONTENT}]
    chat_request(messages)
    print("Starting a phi3 chat. Type 'exit' to quit.")
    debug("Chat is started")
    while(True):
        user_input: str = input("You: ")
        if (user_input.lower() == 'exit'):
            print("Closing the chat. Thank you. Bye!")
            debug("Chat is closed")
            break
        messages.append({
            "role": USER_ROLE,
            "content": user_input
        })
        stop_event: threading.Event = start_thinking_dots("Model is thinking", 0.5)
        response: str = process_LLM(messages)
        stop_event.set()
        print(f"\nAgent: {response}")
        print("_"*60)
