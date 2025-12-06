import requests
from typing import Any, Iterator, Self
from extract_json import extract_json
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
    
    def __iter__(self) -> Iterator[dict]:
        return iter(self.messages)
    
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