from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static, Header, Footer
from textual.containers import Vertical, Horizontal
from api import WeatherAPI, CountryAPI, CurrencyAPI
from storage import FavoritesManager


class CityGuideApp(App):
    CSS = """
    #output {
        padding: 1;
        border: round #666;
        min-height: 10;
    }
    .error { color: red; }
    .success { color: green; }
    """

    def __init__(self):
        super().__init__()
        self.favorites = FavoritesManager()
        self.current_city = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("🌍 City Guide", id="title"),
            Input(placeholder="Enter city name", id="city_input"),
            Horizontal(
                Button("Search", id="search", variant="primary"),
                Button("Favorites", id="favorites"),
                Button("Save", id="save", variant="success"),   # новая кнопка
                Button("Clear", id="clear"),
            ),
            Static("", id="output"),
        )
        yield Footer()

    async def on_button_pressed(self, event):
        button_id = event.button.id
        output = self.query_one("#output")

        if button_id == "clear":
            output.update("")
            self.current_city = None
            output.remove_class("error")
            output.remove_class("success")
        elif button_id == "favorites":
            favs = self.favorites.load()
            output.update("⭐ Favorites:\n" + "\n".join(favs) if favs else "No favorites yet")
        elif button_id == "search":
            await self.search_city()
        elif button_id == "save":
            output.remove_class("error")
            output.remove_class("success")
            if self.current_city and self.favorites.save(self.current_city):
                output.update(f"✅ Saved {self.current_city}!")
                output.add_class("success")
            else:
                output.update(f"{self.current_city} already saved")

    async def search_city(self):
        city = self.query_one("#city_input").value.strip()
        output = self.query_one("#output")

        if not city:
            output.update("Please enter city name")
            output.remove_class("success")
            output.add_class("error")
            return

        try:
            weather = WeatherAPI.get_weather(city)
            country = CountryAPI.get_info(weather['country'])
            rate, _ = CurrencyAPI.get_rate(country['currency'])

            output.update(
                f"📍 {city}\n"
                f"🌡 Temp: {weather['temp']}°C\n"
                f"🌍 Country: {country['name']}\n"
                f"💵 Currency: {rate:.2f} USD\n\n"
                "Press ENTER to save"
            )
            output.remove_class("error")
            self.current_city = city
        except Exception as e:
            output.update(f"Error: {str(e)}", classes="error")
            self.current_city = None

    async def on_input_submitted(self, event):
        if not self.current_city:
            return

        output = self.query_one("#output")
        if self.favorites.save(self.current_city):
            output.update(f"✅ Saved {self.current_city}!", classes="success")
        else:
            output.update(f"{self.current_city} already saved")


if __name__ == "__main__":
    CityGuideApp().run()