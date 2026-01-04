import pytest
import responses
from datetime import datetime
from services.fixer import CurrencyRate, SUCCESS_KEY, RATES_KEY, DATE_KEY, FIXER_DATE_FMT

__mock_key: str = "key"
__mock_url: str = "http://mock.mock"

@responses.activate
def test_get_rate_success() -> None:
    currencyRate: CurrencyRate = CurrencyRate(__mock_url, __mock_key)

    key1, key2 = "key1", "key2"
    __mock_rates: dict[str, float] = { key1: 2.0, key2: 3.0 }
    __mock_response: dict = {
        SUCCESS_KEY: True,
        RATES_KEY: __mock_rates,
        DATE_KEY: datetime.now().strftime(FIXER_DATE_FMT)
    }
    responses.add(responses.GET, url=__mock_url, json=__mock_response, status=200)

    rate: float = currencyRate.get_rate(key1, key2)
    assert rate == pytest.approx(__mock_rates[key2] / __mock_rates[key1], abs=1e-2)

@responses.activate
def test_get_rate_network_error() -> None:
    currencyRate: CurrencyRate = CurrencyRate(__mock_url, __mock_key)
    responses.add(responses.GET, url=__mock_url, status=400)
    with pytest.raises(Exception):
        currencyRate.get_rate("1", "2")