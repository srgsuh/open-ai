from thinking_dots import start_thinking_dots
import threading
from logs import debug
from system_rules import APP_SYSTEM_CONTENT
from chat_request import ChatLLM
from process_llm import process_LLM

def is_exit_request(user_input: str) -> bool:
    return user_input.lower() in ['exit', 'stop', 'quit', 'q']

if __name__ == "__main__":
    debug("Start")
    chat: ChatLLM = ChatLLM(APP_SYSTEM_CONTENT, temperature=0.0)
    print("Starting a phi3 chat. Type 'exit' to quit.")
    debug("Chat is started")
    while(True):
        user_input: str = input("You: ")
        if is_exit_request(user_input):
            print("Closing the chat. Thank you. Bye!")
            debug("Chat is closed")
            break
        chat.user_message(user_input)
        try:
            stop_event: threading.Event = start_thinking_dots("Model is thinking", 0.5)
            response: str = process_LLM(chat)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            stop_event.set()
        print(f"\nAgent: {response}")
        print("_"*60)
