import responses
from tools import get_weather
import os
from unittest import mock

__mock_str: str = "mock"
__mock_num: int = 0
__mock_url: str = "http://mock.mock"
__mock_key: str = "key"
__url: str = f"{__mock_url}?key={__mock_key}&q={__mock_str}&aqi=no"

@responses.activate
def test_mocked_weather_success() -> None:
    condition = {"text": __mock_str}
    location = {"name": __mock_str}
    current = {"condition": condition, "temp_c": __mock_num, "humidity": __mock_num, "wind_kph": __mock_num}
    mock_json = {"location": location,"current": current}

    responses.add(
        method=responses.GET,
        url=__url,
        json=mock_json,
        status=200
    )
    
    with mock.patch.dict(os.environ, {"API_KEY": __mock_key, "URL_CURRENT": __mock_url}):
        res: str = get_weather(__mock_str)
        assert f"Weather in {__mock_str}" in res
        assert f"{__mock_num}°C" in res
        assert f"Wind: {__mock_num} km/h." in res
        assert f"Humidity: {__mock_num}%" in res

@responses.activate
def test_mocked_weather_err() -> None:
    responses.add(
        method=responses.GET,
        url=__url,
        status=400
    )
    with mock.patch.dict(os.environ, {"API_KEY": __mock_key, "URL_CURRENT": __mock_url}):
        res: str = get_weather(__mock_str)
        assert f"Weather forecast in {__mock_str} is unavailable. Error" in res