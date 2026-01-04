import requests
from typing import Any, Self
from services.extract_json import extract_json
from configuration import get_config_parameter

URL: str = "http://localhost:11434/api/chat"
MODEL_NAME: str = "phi3"

def get_url() -> str:
    return get_config_parameter("OLLAMA_URL", URL)

def get_model_name() -> str:
    return get_config_parameter("OLLAMA_MODEL", MODEL_NAME)

class ChatHistory:
    SYS_ROLE: str = "system"
    LLM_ROLE: str = "assistant"
    USER_ROLE: str = "user"
    TOOL_ROLE: str = "tool"

    def __init__(self, system_content: str) -> None:
        self.messages: list[dict] = []
        self.append_message(ChatHistory.SYS_ROLE, system_content)
    
    def append_message(self, role: str, content: str) -> None:
        self.messages.append({ "role": role, "content": content})
    
class ChatLLM:
    def __init__(self, system_content: str, **options) -> None:
        self.__url = get_url()
        self.__model_name = get_model_name()
        self.__history = ChatHistory(system_content)
        if not "temperature" in options:
            options["temperature"] = 0.0
        self.__base_payload: dict[str, Any] = {
            "model": self.__model_name,
            "stream": False,
            "options": options,
            "messages": self.__history.messages
        }
    
    def user_message(self, content: str) -> Self:
        self.__history.append_message(ChatHistory.USER_ROLE, content)
        return self
    
    def tool_message(self, content: str) -> Self:
        self.__history.append_message(ChatHistory.TOOL_ROLE, content)
        return self
    
    def ai_message(self, content: str) -> Self:
        self.__history.append_message(ChatHistory.LLM_ROLE, content)
        return self
    
    def request(self) -> str:
        response = requests.post(self.__url, json=self.__base_payload)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]