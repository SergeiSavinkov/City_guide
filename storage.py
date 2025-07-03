import json
import os
from pathlib import Path


class FavoritesManager:
    """Надёжное хранилище избранных городов"""

    def __init__(self):
        self.file_path = Path("favorites.json")
        self.file_path.parent.mkdir(exist_ok=True)

    def load(self):
        """Загрузка избранного с проверкой файла"""
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r') as f:
                    return json.load(f).get('favorites', [])
            return []
        except Exception:
            return []

    def save(self, city):
        """Сохранение города с проверкой"""
        if not city or not isinstance(city, str):
            return False

        favorites = self.load()
        city = city.strip()

        if city not in favorites:
            favorites.append(city)
            try:
                with open(self.file_path, 'w') as f:
                    json.dump({'favorites': favorites}, f)
                return True
            except Exception:
                return False
        return False