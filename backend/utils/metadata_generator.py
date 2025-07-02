import random
import requests
from datetime import datetime

# Clé API OpenWeatherMap
OPENWEATHER_API_KEY = "eed36ed4831387893d10db8c5891a98d"

# Générer des coordonnées GPS aléatoires dans Paris intra-muros
def get_random_gps_in_paris():
    lat = random.uniform(48.815573, 48.902144)
    lon = random.uniform(2.224199, 2.469920)
    return {"lat": round(lat, 6), "lon": round(lon, 6)}

# Obtenir la météo réelle à partir des coordonnées
def get_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&units=metric&lang=fr&appid={OPENWEATHER_API_KEY}"
    )
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
    except Exception as e:
        print(f"[Erreur météo] {e}")
    return {
        "temperature": None,
        "description": "indisponible",
        "humidity": None,
        "wind_speed": None
    }

# Reverse geocoding (facultatif) pour récupérer le nom du lieu
def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=16"
    headers = {"User-Agent": "cleansight-bot/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Adresse inconnue")
    except Exception as e:
        print(f"[Erreur géocodage] {e}")
    return "Adresse inconnue"

# Fonction principale à appeler dans upload
def generate_metadata():
    coords = get_random_gps_in_paris()
    lat, lon = coords["lat"], coords["lon"]
    weather = get_weather(lat, lon)
    address = reverse_geocode(lat, lon)

    return {
        "timestamp": datetime.now().isoformat(),
        "location": {
            "lat": lat,
            "lon": lon,
            "address": address
        },
        "weather": weather
    }
