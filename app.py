from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static, Header, Footer
from textual.containers import Vertical, Horizontal
from api import WeatherAPI, CountryAPI, CurrencyAPI
from storage import FavoritesManager

class CityGuideApp(App):
    CSS = """
    #title {
        text-style: bold;
        color: cyan;
        padding: 1 0;
        height: auto;
    }
    #output {
        padding: 1 2;
        border: round green;
        min-height: 10;
        margin-top: 1;
    }
    .error {
        color: red;
        text-style: bold;
    }
    .success {
        color: green;
        text-style: bold;
    }
    #city_input {
        border: round #888888;
    }
    Button {
        margin: 0 1;
    }
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
                Button("Save", id="save", variant="success"),
                Button("Clear", id="clear", variant="error"),
                Button("Exit", id="exit", variant="error"),  # основная кнопка выхода
            ),
            Static("", id="output"),
        )
        yield Footer()

    async def on_button_pressed(self, event):
        button_id = event.button.id
        output = self.query_one("#output")
        output.remove_class("error")
        output.remove_class("success")

        if button_id == "clear":
            output.update("")
            self.current_city = None
        elif button_id == "favorites":
            favs = self.favorites.load()
            if favs:
                output.update("⭐ Favorites:\n" + "\n".join(f"• {city}" for city in favs))
            else:
                output.update("⭐ No favorites yet.")
        elif button_id == "search":
            await self.search_city()
        elif button_id == "save":
            if self.current_city:
                if self.favorites.save(self.current_city):
                    output.update(f"✅ Saved {self.current_city} to favorites!")
                    output.add_class("success")
                else:
                    output.update(f"⚠️ {self.current_city} is already in favorites.")
                    output.add_class("error")
            else:
                output.update("⚠️ No city to save. Please search first.")
                output.add_class("error")
        elif button_id == "exit":
            self.exit()  # мгновенный выход без подтверждений

    async def search_city(self):
        city = self.query_one("#city_input").value.strip()
        output = self.query_one("#output")
        output.remove_class("error")
        output.remove_class("success")

        if not city:
            output.update("⚠️ Please enter a city name.")
            output.add_class("error")
            return

        try:
            weather = WeatherAPI.get_weather(city)
            country = CountryAPI.get_info(weather['country'])
            rate, _ = CurrencyAPI.get_rate(country['currency'])
            output.update(
                f"📍 [b]{city}[/b]\n"
                f"🌡  Temperature: {weather['temp']}°C\n"
                f"🌍 Country: {country['name']}\n"
                f"💱 1 {country['currency']} = {rate:.2f} USD"
            )
            output.add_class("success")
            self.current_city = city
        except Exception as e:
            output.update(f"❌ Error: {str(e)}")
            output.add_class("error")
            self.current_city = None

    async def on_input_submitted(self, event):
        pass

if __name__ == "__main__":
    CityGuideApp().run()