from system_rules import INNER_SYSTEM_CONTENT
import re
import json
from logs import debug
from chat_request import ChatLLM
from extract_json import extract_json
from fixer import CURRENCY_RATE

def travel_info(country_from: str, country_to: str, code_from: str) -> str:
    result: dict[str, str | float]
    try:
        chat = ChatLLM(INNER_SYSTEM_CONTENT, temperature=0.0)
        raw_reply: str = chat.user_message(f"The currency of {country_to}").request()
        json_reply: dict = extract_json(raw_reply, ["country", "currency_name", "currency_code"]) or {}
        code_to: str = json_reply["currency_code"]
        rate = CURRENCY_RATE.get_rate(code_from, code_to)
        result = {
            "country_from": country_from,
            "code_from": code_from,
            "country_to": country_to,
            "code_to": code_to,
            "exchange_rate": rate
        }
    except Exception as e:
        result = {"error" : str(e)}
    
    return json.dumps(result)