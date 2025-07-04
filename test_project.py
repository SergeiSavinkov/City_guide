import pytest
from unittest.mock import patch

from storage import FavoritesManager
from api import WeatherAPI, CountryAPI, CurrencyAPI

# FavoritesManager tests
def test_load_returns_empty_for_missing_file(tmp_path):
    fm = FavoritesManager()
    fm.file_path = tmp_path / "favorites.json"
    assert fm.load() == []

def test_save_new_city_and_load(tmp_path):
    fm = FavoritesManager()
    fm.file_path = tmp_path / "favorites.json"
    assert fm.save("London")
    assert fm.load() == ["London"]

def test_save_duplicate_city(tmp_path):
    fm = FavoritesManager()
    fm.file_path = tmp_path / "favorites.json"
    fm.save("London")
    assert not fm.save("London")

def test_save_invalid_city(tmp_path):
    fm = FavoritesManager()
    fm.file_path = tmp_path / "favorites.json"
    assert not fm.save(None)
    assert not fm.save("")
    assert not fm.save(123)

def test_load_fails_on_invalid_json(tmp_path):
    invalid_path = tmp_path / "favorites.json"
    invalid_path.write_text("{invalid_json:}")
    fm = FavoritesManager()
    fm.file_path = invalid_path
    assert fm.load() == []

# WeatherAPI tests (using mock)
@patch("api.requests.get")
def test_weatherapi_get_weather_success(mock_get):
    mock_get.return_value.json.return_value = {
        "main": {"temp": 15},
        "weather": [{"description": "sunny"}],
        "sys": {"country": "GB"}
    }
    mock_get.return_value.raise_for_status.return_value = None
    result = WeatherAPI.get_weather("London")
    assert result['temp'] == 15
    assert result['country'] == "GB"
    assert result['description'] == "sunny"

@patch("api.requests.get")
def test_weatherapi_get_weather_failure(mock_get):
    mock_get.side_effect = Exception("API error")
    with pytest.raises(Exception):
        WeatherAPI.get_weather("Nowhere")

# CountryAPI tests (using mock)
@patch("api.requests.get")
def test_countryapi_get_info_success(mock_get):
    mock_get.return_value.json.return_value = [{
        "name": {"common": "United Kingdom"},
        "currencies": {"GBP": {}},
        "region": "Europe"
    }]
    mock_get.return_value.raise_for_status.return_value = None
    info = CountryAPI.get_info("GB")
    assert info['name'] == "United Kingdom"
    assert info['currency'] == "GBP"
    assert info['region'] == "Europe"

@patch("api.requests.get")
def test_countryapi_get_info_error(mock_get):
    mock_get.side_effect = Exception()
    info = CountryAPI.get_info("XX")
    assert info['name'] == "Unknown"
    assert info['currency'] is None

# CurrencyAPI tests (using mock)
@patch("api.requests.get")
def test_currencyapi_get_rate_success(mock_get):
    mock_get.return_value.json.return_value = {
        "rates": {"USD": 1.3}
    }
    rate, text = CurrencyAPI.get_rate("GBP")
    assert rate == 1.3
    assert text == "Current rate"

def test_currencyapi_get_rate_missing_currency():
    rate, text = CurrencyAPI.get_rate(None)
    assert rate == 0.0

@patch("api.requests.get")
def test_currencyapi_get_rate_api_error(mock_get):
    mock_get.side_effect = Exception()
    rate, text = CurrencyAPI.get_rate("GBP")
    assert rate == 0.0