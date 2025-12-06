from thinking_dots import ThinkingDots
from logs import debug
from system_rules import APP_SYSTEM_CONTENT
from chat_request import ChatLLM
from process_llm import process_LLM

def is_exit_request(user_input: str) -> bool:
    return user_input.lower() in ['exit', 'stop', 'quit', 'q']

if __name__ == "__main__":
    debug("Start")
    chat: ChatLLM = ChatLLM(APP_SYSTEM_CONTENT)
    print("Starting a phi3 chat. Type 'exit' to quit.")
    debug("Chat is started")
    while(True):
        user_input: str = input("You: ")
        if is_exit_request(user_input):
            print("Closing the chat. Thank you. Bye!")
            debug("Chat is closed")
            break
        chat.user_message(user_input)
        with ThinkingDots("Model is thinking"):
            response: str = process_LLM(chat)
        print(f"\nAgent: {response}")
        print("_"*60)
