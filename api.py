import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Получение погоду по названию города
class WeatherAPI:
    API_KEY = os.getenv("OPEN_WEATHER_KEY")

    @classmethod
    # Возвращает температуру, описание погоды и код страны для указанного города
    def get_weather(cls, city):
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    'q': city,
                    'appid': cls.API_KEY,
                    'units': 'metric'
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return {
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'country': data['sys']['country']
            }
        except Exception as e:
            raise Exception(f"Weather error: {str(e)}")

# Получает информацию о стране по её коду (например, RU, GB)
class CountryAPI:
    @classmethod
    # Возвращает название страны, валюту и регион, используя сервис restcountries.com
    def get_info(cls, country_code):
        try:
            response = requests.get(
                f"https://restcountries.com/v3.1/alpha/{country_code}",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()[0]
            currency = list(data['currencies'].keys())[0] if 'currencies' in data else None
            return {
                'name': data['name']['common'],
                'currency': currency,
                'region': data['region']
            }
        except Exception:
            return {
                'name': 'Unknown',
                'currency': None,
                'region': 'Unknown'
            }

# Получает курс валюты к доллару США
class CurrencyAPI:
    @classmethod
    # Возвращает курс указанной валюты к USD через сервис exchangerate-api.com
    def get_rate(cls, base_currency):
        if not base_currency:
            return 0.0, "No currency"

        try:
            response = requests.get(
                "https://api.exchangerate-api.com/v4/latest/" + base_currency,
                timeout=5
            )
            data = response.json()
            return data['rates']['USD'], "Current rate"
        except Exception:
            return 0.0, "Rate unavailable"