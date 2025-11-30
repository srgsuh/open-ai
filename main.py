import requests
from typing import Any

URL: str = "http://localhost:11434/api/chat"
MODEL_NAME: str = "phi3"

def chat_request(messages: list) -> str:
    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }
    response = requests.post(URL, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]

if __name__ == "__main__":
    messages = [
        {
            "role": "System",
            "content": "You should answer clearly and briefly."
        }
    ]
    chat_request(messages)
    print("Starting a phi3 chat. Type 'exit' to quit.")
    while(True):
        user_input: str = input("You: ")
        if (user_input.lower() == 'exit'):
            print("Closing the chat. Thank you. Bye!")
            break
        messages.append({
            "role": "user",
            "content": user_input
        })
        reply = chat_request(messages)
        messages.append({
            "role": "assistant",
            "content": reply
        })
        print(f"\nAgent: {reply}")
        print("_"*60)
