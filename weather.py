import requests
import os

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat: float, lon: float):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"]
        }
    return {"temperature": "NA", "humidity": "NA", "condition": "NA"}
