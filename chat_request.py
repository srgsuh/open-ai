import requests
from typing import Any, Self
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
    
    def append_message(self, role: str, content: str) -> None:
        self.messages.append({ "role": role, "content": content})
    
class ChatLLM:
    def __init__(self, system_content: str, **options) -> None:
        self.__url = URL
        self.__base_payload: dict[str, Any] = {
            "model": MODEL_NAME,
            "stream": False,
            "options": options
        }
        self.__history = ChatHistory()
        self.__history.append_message(ChatHistory.SYS_ROLE, system_content)
    
    def user_message(self, content: str) -> Self:
        self.__history.append_message(ChatHistory.USER_ROLE, content)
        return self
    
    def tool_message(self, content: str) -> Self:
        self.__history.append_message(ChatHistory.TOOL_ROLE, content)
        return self
    
    def ai_message(self, content: str) -> Self:
        self.__history.append_message(ChatHistory.LLM_ROLE, content)
        return self
    
    def _payload(self) -> dict[str, Any]:
        return {"messages": self.__history.messages, **self.__base_payload}
    
    def request(self) -> str:
        response = requests.post(self.__url, json=self._payload())
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]