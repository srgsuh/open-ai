from system_rules import INNER_SYSTEM_CONTENT
import json
from logs import debug
from chat_request import ChatLLM
from extract_json import extract_json
from fixer import CURRENCY_RATE

COUNTRY: str = "country"
CUR_NAME: str = "currency_name"
CUR_CODE: str = "currency_code"

def travel_info(country_from: str, country_to: str, code_from: str) -> str:
    result: dict[str, str | float]
    try:
        raw_reply: str = ChatLLM(INNER_SYSTEM_CONTENT).user_message(f"The currency of {country_to}").request()
        json_reply: dict = extract_json(raw_reply, [COUNTRY, CUR_NAME, CUR_CODE]) or {}
        rate = CURRENCY_RATE.get_rate(code_from, json_reply[CUR_CODE])
        result = {
            "country_from": country_from,
            "code_from": code_from,
            "country_to": json_reply[COUNTRY],
            "code_to": json_reply[CUR_CODE],
            "currency_to": json_reply[CUR_NAME],
            "exchange_rate": rate
        }
    except Exception as e:
        result = {"error" : str(e)}
    debug(f"travel_info. result={result}")
    return json.dumps(result)