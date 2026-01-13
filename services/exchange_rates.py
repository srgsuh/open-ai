from configuration import get_config_parameter
import requests
from logs import logger

RATE_DEFAULT_URL: str = "https://api.exchangerate.host"

BASE_CUR_CODE: str = "USD"

BASE_PARAMETERS: dict = {}
CURRENCIES: dict[str, str] = {}
RATES: dict[str, float] = {}

def get_api_key() -> str:
    return get_config_parameter("RATE_API_KEY")

def get_base_url() -> str:
    return get_config_parameter("RATE_URL", RATE_DEFAULT_URL)

def get_base_parameters() -> dict:
    global BASE_PARAMETERS
    if not BASE_PARAMETERS:
        BASE_PARAMETERS = {"access_key": get_api_key()}
    
    return BASE_PARAMETERS

def get_request_parameters(**kwargs) -> dict:
    params: dict = get_base_parameters().copy()
    params.update(kwargs)
    return params

def get_currency_names() -> dict:
    global CURRENCIES
    if not CURRENCIES:
        response = requests.get(f"{get_base_url()}/list", params=get_base_parameters())
        response.raise_for_status()
        data = response.json()
        CURRENCIES = data.get("currencies", {})
    
    return CURRENCIES

def _extract_rates(src_code: str, src_rates: dict) -> dict[str, float]:
    extracted_rates: dict = {}
    for code, rate in src_rates.items():
        if code.startswith(src_code):
            extracted_rates[code[len(src_code):]] = float(rate)
    if src_code not in extracted_rates:
        extracted_rates[src_code] = 1.0
    return extracted_rates

def get_rates() -> dict:
    global RATES
    if not RATES:
        response = requests.get(f"{get_base_url()}/live", params=get_base_parameters())
        response.raise_for_status()
        data = response.json()
        src_rates = data.get("quotes", {})
        src_code = data.get("source", BASE_CUR_CODE)
        RATES = _extract_rates(src_code, src_rates)
    
    return RATES

def _get_exchange_rate(code_from: str, code_to: str) -> float:
    rates = get_rates()
    def _get_rate(code: str) -> float:
        rate = rates.get(code)
        if rate is None:
            raise ValueError(f"Unsupported currency code: {code}")
        return rate
    
    rate_from = _get_rate(code_from)
    rate_to = _get_rate(code_to)
    return rate_to / rate_from

def get_exchange_rate(code_from: str, code_to: str) -> float | None:
    rate: float | None = None
    try:
        rate = _get_exchange_rate(code_from, code_to)
    except Exception as e:
        logger.exception("Error retrieving exhange rate", str(e))

    return rate

def get_exchange_rate_data(code_from: str, code_to: str, is_full_names: bool = False) -> dict:
    try:
        rate = _get_exchange_rate(code_from, code_to)
        rate_data = {
            "currency_from": code_from,
            "currency_to": code_to,
            "exchange_rate": rate
        }
        if is_full_names:
            currencies = get_currency_names()
            rate_data["currency_from_name"] = currencies.get(code_from, "Unknown currency name")
            rate_data["currency_to_name"] = currencies.get(code_to, "Unknown currency name")
        
        return rate_data
    except Exception as e:
        return {
            "error": str(e)
        }