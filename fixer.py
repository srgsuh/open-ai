import requests
from configuration import get_config_parameter
from datetime import datetime

SUCCESS_KEY: str = "success"
RATES_KEY: str = "rates"
DATE_KEY: str = "date"
FIXER_DATE_FMT: str = get_config_parameter("FIXER_DATE_FMT", "%Y-%m-%d")

def __get_url() -> str:
    return get_config_parameter("FIXER_URL")

def __get_api_key() -> str:
    return get_config_parameter("FIXER_API_KEY")

class CurrencyRate:
    def __init__(self, url: str, api_key: str) -> None:
        self.__url = url
        self.__params = {"access_key" : api_key}
        self.__latest_date: str = ""
        self.__latest_cache: dict = {}
    
    def update_rates(self) -> None:
        response = requests.get(self.__url, params=self.__params)
        response.raise_for_status()
        response_json: dict = response.json()
        self.__latest_date = response_json[DATE_KEY]
        self.__latest_cache = response_json[RATES_KEY]

    def __check_cache(self) -> None:
        today: str = datetime.now().strftime(FIXER_DATE_FMT)
        if not (self.__latest_date == today):
            self.update_rates()

    def get_rate(self, code_from: str, code_to: str) -> float:
        def get_euro_rate(code: str) -> float:
            if not code in self.__latest_cache:
                raise ValueError(f"Currency code {code} is not supported")
            return self.__latest_cache[code]

        self.__check_cache()
        return get_euro_rate(code_to) / get_euro_rate(code_from)

CURRENCY_RATE: CurrencyRate = CurrencyRate(__get_url(), __get_api_key())