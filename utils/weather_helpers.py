import requests

# Use your actual API key here
API_KEY_OPENWEATHER = "ddcaaa2b45b511ae9ea37a8633d8aa66"

def get_cloud_coverage(latitude, longitude):
    """Fetch cloud coverage for a location using OpenWeatherMap API."""
    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"lat": latitude, "lon": longitude, "appid": API_KEY_OPENWEATHER}
    try:
        response = requests.get(weather_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        cloud_percent = data.get("clouds", {}).get("all", 0)
        return cloud_percent
    except Exception as error:
        print(f"Error fetching cloud coverage: {error}")
        return 100

def calculate_visibility(cloud_percent, is_night_time):
    """Return visibility status based on clouds and night/day."""
    if not is_night_time:
        return "It is daytime and not visible"
    if cloud_percent < 30:
        return "High"
    elif cloud_percent < 60:
        return "Medium"
    else:
        return "Low"



def get_weather_data(latitude, longitude, is_night_time=True):
    """Return temperature, cloud percent, visibility, description."""
    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY_OPENWEATHER,
        "units": "metric"
    }
    try:
        response = requests.get(weather_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        temperature_celsius = data.get("main", {}).get("temp", None)
        temperature_fahrenheit = temperature_celsius * 9/5 + 32 if temperature_celsius is not None else None
        cloud_percent = data.get("clouds", {}).get("all", 0)
        description = data.get("weather", [{}])[0].get("description", "No data").capitalize()
        visibility = "High" if is_night_time and cloud_percent < 30 else \
                     "Medium" if is_night_time and cloud_percent < 60 else \
                     "Low"

        return {
            "temperature_celsius": temperature_celsius,
            "temperature_fahrenheit": temperature_fahrenheit,
            "cloud_percent": cloud_percent,
            "description": description,
            "visibility": visibility
        }

    except Exception as error:
        print(f"Error fetching weather: {error}")
        return {
            "temperature_celsius": None,
            "temperature_fahrenheit": None,
            "cloud_percent": 100,
            "description": "No data",
            "visibility": "Low"
        }
