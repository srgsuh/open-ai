import requests
from configuration import get_config_parameter
from datetime import datetime

SUCCESS_KEY: str = "success"
RATES_KEY: str = "rates"
DATE_KEY: str = "date"
FIXER_DATE_FMT: str = "%Y-%m-%d"

class CurrencyRequestError(RuntimeError):
    pass

def __get_url() -> str:
    return get_config_parameter("FIXER_URL")

def __get_api_key() -> str:
    return get_config_parameter("FIXER_API_KEY")

class CurrencyRate:
    def __init__(self, url, api_key) -> None:
        self.__url = url
        self.__api_key = api_key
        self.__latest_date: str = ""
        self.__latest_cache: dict = {}
    
    def __get_latest_raw(self) -> dict:
        response = requests.get(self.__url, params={"access_key" : self.__api_key})
        response.raise_for_status()
        return response.json()

    def __load_rates(self) -> None:
        raw_response: dict = self.__get_latest_raw()
        if not raw_response[SUCCESS_KEY]:
            raise CurrencyRequestError("Currency data is unavailable now. Try again later.")
        
        self.__latest_date = raw_response[DATE_KEY]
        self.__latest_cache = raw_response[RATES_KEY]

    def __get_latest(self) -> None:
        today: str = datetime.now().strftime(FIXER_DATE_FMT)
        if not (self.__latest_date == today):
            self.__load_rates()

    def get_rate(self, code_from: str, code_to: str) -> float:
        self.__get_latest()
        def get_euro_rate(code: str) -> float:
            if not code in self.__latest_cache:
                raise ValueError(f"Currency code {code} is not supported")
            return self.__latest_cache[code]
    
        return get_euro_rate(code_to) / get_euro_rate(code_from)

CURRENCY_RATE: CurrencyRate = CurrencyRate(__get_url(), __get_api_key())

if __name__ == "__main__":
    rate: float = CURRENCY_RATE.get_rate('USD', 'GBP')
    print(f"1 dollar = {rate} pounds")