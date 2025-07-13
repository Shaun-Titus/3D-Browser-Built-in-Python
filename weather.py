import requests

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city="Kottayam"):
    params = {"q": city, "units": "metric", "appid": API_KEY}
    try:
        resp = requests.get(API_URL, params=params, timeout=5)
        data = resp.json()
        return {
            "temp": round(data["main"]["temp"]),
            "cond": data["weather"][0]["main"],
            "icon": data["weather"][0]["icon"],
        }
    except Exception:
        return {"temp": "--", "cond": "N/A", "icon": ""}
