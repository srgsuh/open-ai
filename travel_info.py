from system_rules import INNER_SYSTEM_CONTENT
import re
import json
from logs import debug
from chat_request import ChatLLM
from extract_json import extract_json

def travel_info(country_from: str, country_to: str, code_from: str) -> str:
    chat = ChatLLM(INNER_SYSTEM_CONTENT)
    chat.user_message(f"The currency of {country_to}")

    debug(f"Requesting data about {country_to}")
    raw_reply: str = chat.request()
    debug(f"Data about {country_to} = {raw_reply}")
    json_reply: dict = extract_json(raw_reply, ["country", "currency_name", "currency_code"]) or {}
    debug(f"Parsed data about {country_to} = {json_reply}")
    code_to: str = json_reply.get("currency_code", "unknown")
        
    return (f"Travel from {country_from} to {country_to}, code_from={code_from}, code_to={code_to}")