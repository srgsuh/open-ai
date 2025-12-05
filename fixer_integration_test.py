import pytest
import responses
from fixer import get_rate, SUCCESS_KEY, RATES_KEY
import json

__mock_key: str = "key"
__mock_url: str = "http://mock.mock"

@responses.activate
def test_get_rate_success(monkeypatch) -> None:
    monkeypatch.setenv("FIXER_URL", __mock_url)
    monkeypatch.setenv("FIXER_API_KEY", __mock_url)
    key1, key2 = "key1", "key2"
    __mock_rates: dict[str, float] = { key1: 2.0, key2: 3.0 }
    __mock_response: dict = {
        SUCCESS_KEY: True,
        RATES_KEY: __mock_rates
    }
    responses.add(responses.GET, url=__mock_url, json=__mock_response, status=200)

    rate: float = get_rate(key1, key2)
    assert rate == pytest.approx(__mock_rates[key2] / __mock_rates[key1])
