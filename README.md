# City Guide

**City Guide** is an interactive Python TUI application that lets you check the current weather, basic country information, and currency rate for any chosen city—and save your favorite cities locally.

## Features

- View up-to-date weather for a selected city
- Get information about the city's country and local currency
- See the latest currency exchange rate against USD
- Save cities as favorites for quick access
- View your list of favorite cities at any time
- View all favorite cities on an interactive map
- User-friendly text interface powered by [Textual](https://textual.textualize.io/)

## Requirements

- Python 3.9+
- `requests`
- `python-dotenv`
- `textual`
- `folium`

## Quick Start

1. **Clone the repository and navigate to the project folder:**
    ```bash
    git clone <your-repo-url>
    cd <project-folder>
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` file in the project root and add your OpenWeather API key:**
    ```
    OPEN_WEATHER_KEY=your_openweather_api_key
    ```

4. **Run the application:**
    ```bash
    python app.py
    ```

## How to Use

- Enter the city name in the input field.
- Click `Search` to display information about the city.
- Click `Save` to add the current city to your favorites.
- Use the `Favorites` button to view your list of saved cities.
- Click `Show Map` to see all your saved cities on an interactive map.
The map will be saved as `favorites_map.html` and should open automatically in your browser.
- Use the `Clear` button to clear the output area.
- Click `Exit` to exit the program.

## Architecture Overview

- **api.py** — Contains classes for working with external APIs: weather (OpenWeather), country information (REST Countries), and exchange rates (exchangerate-api).
- **geo.py** — Handles map-related functionality, including generating and saving a map of favorite cities.
- **app.py** — Main script implementing TUI logic based on Textual.
- **storage.py** — Manages favorite cities, storing them in `favorites.json`.

## Data Storage

Favorite cities are saved in the `favorites.json` file in the project’s root directory. Your data is always recoverable or portable as needed.

## License

For educational and demonstration purposes only.

---

For questions or suggestions, feel free to open an issue!