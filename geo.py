from geopy.geocoders import Nominatim

def get_lat_lon(city):
    # Создание объекта геолокатора для работы с Nominatim
    geolocator = Nominatim(user_agent="city_guide_app")
    # Выполняет поиск координат по названию города
    # Если город найден, возвращает его широту и долготу
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    # Не найден, return None
    return None, None