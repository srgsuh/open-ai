from system_rules import INNER_SYSTEM_CONTENT
import re
import json
from logs import debug
from chat_request import chat_request, ChatHistory

def extract_json(text: str) -> dict | None:
    json_re: str = r"\{.*country.*currency_name.*currency_code.*\}"
    match: re.Match | None = re.search(json_re, text, re.DOTALL)
    
    result: dict | None = None
    if match:
        try:
            result = json.loads(match.group())
        except Exception:
            pass
    
    return result

def travel_info(country_from: str, country_to: str, code_from: str) -> str:
    history = ChatHistory().sys_message(INNER_SYSTEM_CONTENT)
    history.user_message(f"The currency of {country_to}")

    debug(f"Requesting data about {country_to}")
    raw_reply: str = chat_request(history)
    debug(f"Data about {country_to} = {raw_reply}")
    json_reply: dict = extract_json(raw_reply) or {}
    debug(f"Parsed data about {country_to} = {json_reply}")
    code_to: str = json_reply.get("currency_code", "unknown")
        
    return (f"Travel from {country_from} to {country_to}, code_from={code_from}, code_to={code_to}")