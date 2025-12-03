import requests
from typing import Any, Callable
from tools import TOOLS
from system_content import SYSTEM_CONTENT
import re
import json
from thinking_dots import start_thinking_dots
import threading
from logs import debug

URL: str = "http://localhost:11434/api/chat"
MODEL_NAME: str = "phi3"

def chat_request(messages: list) -> str:
    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.05}
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

def process_LLM(text: str) -> dict:
    res: dict = {
        "role": "assistant",
        "content": text
    }
    tool_data: dict | None = extract_json(text)
    if tool_data:
        tool_response: str = call_tool(tool_data)
        if tool_response:
            res = {
                "role": "tool",
                "content": json.dumps({"result": tool_response})
            }

    return res


if __name__ == "__main__":
    debug("Start")
    messages = [
        {
            "role": "System",
            "content": SYSTEM_CONTENT
        }
    ]
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
            "role": "user",
            "content": user_input
        })
        stop_event: threading.Event = start_thinking_dots("Model is thinking", 0.5)
        reply: str = chat_request(messages)
        response: dict = process_LLM(reply)
        stop_event.set()
        messages.append(response)
        print(f"\nAgent: {response["content"]}")
        print("_"*60)
