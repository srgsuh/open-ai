from typing import Callable
from tools import TOOLS
from system_content import SYSTEM_CONTENT
from thinking_dots import start_thinking_dots
import threading
from logs import debug
from system_rules import APP_SYSTEM_CONTENT
from chat_request import chat_request, process_LLM, ChatHistory

if __name__ == "__main__":
    debug("Start")
    history: ChatHistory = ChatHistory()
    history.sys_message(APP_SYSTEM_CONTENT)
    chat_request(history)
    print("Starting a phi3 chat. Type 'exit' to quit.")
    debug("Chat is started")
    while(True):
        user_input: str = input("You: ")
        if (user_input.lower() == 'exit'):
            print("Closing the chat. Thank you. Bye!")
            debug("Chat is closed")
            break
        history.user_message(user_input)
        stop_event: threading.Event = start_thinking_dots("Model is thinking", 0.5)
        response: str = process_LLM(history)
        stop_event.set()
        print(f"\nAgent: {response}")
        print("_"*60)
