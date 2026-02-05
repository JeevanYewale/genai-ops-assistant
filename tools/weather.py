from crewai import Tool
import httpx


def geocode_city(city: str) -> tuple:
    """Geocode city using Nominatim (OpenStreetMap) - free, no key"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        resp = httpx.get(
            url,
            params={"q": city, "format": "json"},
            headers={"User-Agent": "ai-ops-assistant"},
            timeout=10.0,
        )
        resp.raise_for_status()

        data = resp.json()
        if not data:
            raise ValueError(f"City '{city}' not found")

        return float(data[0]["lat"]), float(data[0]["lon"])

    except Exception as e:
        raise Exception(f"Geocoding error: {str(e)}")


def get_weather(city: str) -> str:
    """Get current weather for a city using Open-Meteo API"""
    try:
        lat, lon = geocode_city(city)

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&timezone=auto"
        resp = httpx.get(url, timeout=10.0)
        resp.raise_for_status()

        data = resp.json()
        temp = data["current"]["temperature_2m"]
        code = data["current"]["weather_code"]

        condition_map = {
            0: "Clear",
            1: "Partly Cloudy",
            2: "Cloudy",
            3: "Overcast",
            45: "Foggy",
            61: "Rain",
            80: "Heavy Rain",
            95: "Thunderstorm",
        }
        condition = condition_map.get(code, "Unknown")

        return f"Weather in {city}: {temp}°C, {condition} [Open-Meteo API]"

    except Exception as e:
        return f"Error fetching weather: {str(e)}"


WeatherTool = Tool.from_function(
    name="weather_tool",
    description="Get current weather by city (uses Nominatim geocoding)",
    func=get_weather,
)
