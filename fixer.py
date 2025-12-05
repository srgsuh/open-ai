import requests
from configuration import get_config_parameter

SUCCESS_KEY: str = "success"
RATES_KEY: str = "rates"

class CurrencyRequestError(RuntimeError):
    pass

def get_url() -> str:
    return get_config_parameter("FIXER_URL")

def get_query_params() -> dict[str, str]:
    api_key: str = get_config_parameter("FIXER_API_KEY")
    return {"access_key" : api_key}

def get_latest_raw() -> dict:
    response = requests.get(get_url(), params=get_query_params())
    response.raise_for_status()
    return response.json()

def get_latest() -> dict:
    raw_response: dict = get_latest_raw()
    if not raw_response[SUCCESS_KEY]:
        raise CurrencyRequestError("Currency data is unavailable now. Try again later.")
    
    return raw_response[RATES_KEY]

def calculate_rate(euro_rates: dict, code_from: str, code_to: str) -> float:
    def get_euro_rate(code: str) -> float:
        if not code in euro_rates:
            raise ValueError(f"Currency code {code} is not supported")
        return euro_rates[code]
    
    return get_euro_rate(code_to) / get_euro_rate(code_from)

def get_rate(code_from: str, code_to: str) -> float:
    latest: dict = get_latest()
    return calculate_rate(euro_rates=latest, code_from=code_from, code_to=code_to)

if __name__ == "__main__":
    print(get_latest())
    print(get_rate('USD', 'GBP'))