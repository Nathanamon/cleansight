import random
import requests
from datetime import datetime
import time

# Clé API OpenWeatherMap
OPENWEATHER_API_KEY = "eed36ed4831387893d10db8c5891a98d"

def get_random_gps_in_paris():
    lat = random.uniform(48.815573, 48.902144)
    lon = random.uniform(2.224199, 2.469920)
    return {"lat": round(lat, 6), "lon": round(lon, 6)}

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

def reverse_geocode(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=16&addressdetails=1"
    headers = {"User-Agent": "cleansight-bot/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            address = data.get("display_name", "Adresse inconnue")
            postcode = data.get("address", {}).get("postcode", "")
            return address, postcode
    except Exception as e:
        print(f"[Erreur géocodage] {e}")
    return "Adresse inconnue", ""

def generate_metadata():
    for _ in range(10):  # 10 essais max
        coords = get_random_gps_in_paris()
        lat, lon = coords["lat"], coords["lon"]
        address, postcode = reverse_geocode(lat, lon)
        
        if postcode.startswith("750"):  # Valide pour Paris intra-muros
            weather = get_weather(lat, lon)
            return {
                "timestamp": datetime.now().isoformat(),
                "location": {
                    "lat": lat,
                    "lon": lon,
                    "address": address
                },
                "weather": weather
            }

        time.sleep(1)  # éviter de spammer l'API Nominatim

    # Si aucun point valide trouvé
    print("[Erreur] Aucune adresse Paris intra-muros trouvée après 10 essais.")
    return None
