"""
Live Weather Intelligence Service
Queries OpenWeatherMap for major Indian agricultural regions and computes
disease-favorable weather risk zones in real-time.
Results are cached for 30 minutes to avoid API rate limits.
"""

import os
import time
import requests
from typing import List, Dict, Any

WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")

# ── Major Indian Agricultural Regions ──────────────────────────────────────
# Each entry: (city_name, state, lat, lon, primary_crops)
AGRICULTURAL_CITIES = [
    # North India — Wheat, Rice, Apple belt
    ("Shimla", "Himachal Pradesh", 31.1048, 77.1734, ["Apple", "Cherry"]),
    ("Srinagar", "J&K", 34.0837, 74.7973, ["Apple", "Cherry"]),
    ("Kullu", "Himachal Pradesh", 31.9579, 77.1095, ["Apple"]),
    ("Ludhiana", "Punjab", 30.9010, 75.8573, ["Wheat", "Rice"]),
    ("Karnal", "Haryana", 29.6857, 76.9905, ["Wheat", "Rice"]),
    ("Agra", "Uttar Pradesh", 27.1767, 78.0081, ["Potato", "Tomato"]),
    ("Lucknow", "Uttar Pradesh", 26.8467, 80.9462, ["Wheat", "Rice", "Squash"]),

    # Central India — Soybean, Cotton
    ("Indore", "Madhya Pradesh", 22.7196, 75.8577, ["Soybean", "Wheat"]),
    ("Nagpur", "Maharashtra", 21.1458, 79.0882, ["Orange", "Cotton", "Soybean"]),
    ("Bhopal", "Madhya Pradesh", 23.2599, 77.4126, ["Wheat", "Soybean"]),

    # West India — Grape, Tomato, Onion
    ("Nashik", "Maharashtra", 19.9975, 73.7898, ["Grape", "Tomato", "Onion"]),
    ("Pune", "Maharashtra", 18.5204, 73.8567, ["Tomato", "Grape"]),
    ("Sangli", "Maharashtra", 16.8524, 74.5815, ["Grape", "Sugarcane"]),
    ("Ahmedabad", "Gujarat", 23.0225, 72.5714, ["Cotton", "Groundnut"]),

    # South India — Rice, Chili, Cotton
    ("Hyderabad", "Telangana", 17.3850, 78.4867, ["Rice", "Cotton", "Chili"]),
    ("Guntur", "Andhra Pradesh", 16.3067, 80.4365, ["Pepper", "Chili", "Cotton", "Tobacco"]),
    ("Kurnool", "Andhra Pradesh", 15.8281, 78.0373, ["Tomato", "Cotton", "Corn"]),
    ("Bangalore", "Karnataka", 12.9716, 77.5946, ["Tomato", "Grape"]),
    ("Coimbatore", "Tamil Nadu", 11.0168, 76.9558, ["Cotton", "Coconut"]),
    ("Thanjavur", "Tamil Nadu", 10.7870, 79.1378, ["Rice"]),
    ("Cuttack", "Odisha", 20.4625, 85.8830, ["Rice"]),

    # East India — Rice, Jute, Tea
    ("Kolkata", "West Bengal", 22.5726, 88.3639, ["Rice", "Jute"]),
    ("Patna", "Bihar", 25.6093, 85.1376, ["Rice", "Wheat", "Corn", "Potato"]),
    ("Jorhat", "Assam", 26.7509, 94.2037, ["Tea", "Rice"]),
]

# ── Cache ──────────────────────────────────────────────────────────────────
_weather_cache: Dict[str, Any] = {}
_cache_timestamp: float = 0
CACHE_DURATION = 1800  # 30 minutes


def calculate_risk(temp: float, humidity: float) -> str:
    """Compute disease spread risk from weather parameters."""
    if humidity > 75 and 18 <= temp <= 28:
        return "HIGH"
    elif humidity > 60 and 15 <= temp <= 32:
        return "MEDIUM"
    else:
        return "LOW"


def fetch_weather_for_cities() -> List[Dict[str, Any]]:
    """
    Query OpenWeatherMap for all agricultural cities and compute risk.
    Returns cached results if available and fresh (< 30 min old).
    """
    global _weather_cache, _cache_timestamp

    # Return cache if fresh
    if _weather_cache and (time.time() - _cache_timestamp) < CACHE_DURATION:
        return _weather_cache.get("zones", [])

    if not WEATHER_API_KEY:
        # Return mock risk data if no API key
        return _generate_mock_weather()

    zones = []
    for city, state, lat, lon, crops in AGRICULTURAL_CITIES:
        try:
            url = (
                f"http://api.openweathermap.org/data/2.5/weather"
                f"?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
            )
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data.get("wind", {}).get("speed", 0)
            description = data.get("weather", [{}])[0].get("description", "")
            risk = calculate_risk(temp, humidity)

            zones.append({
                "city": city,
                "state": state,
                "latitude": lat,
                "longitude": lon,
                "crops": crops,
                "temperature": round(temp, 1),
                "humidity": round(humidity, 1),
                "wind_speed": round(wind, 1),
                "weather_desc": description,
                "risk": risk,
                "radius_km": 60 if risk == "HIGH" else 40 if risk == "MEDIUM" else 25,
            })
        except Exception as e:
            print(f"Weather fetch failed for {city}: {e}")
            # Still add with unknown risk so the city appears
            zones.append({
                "city": city,
                "state": state,
                "latitude": lat,
                "longitude": lon,
                "crops": crops,
                "temperature": None,
                "humidity": None,
                "wind_speed": None,
                "weather_desc": "unavailable",
                "risk": "UNKNOWN",
                "radius_km": 30,
            })

    # Cache the results
    _weather_cache = {"zones": zones}
    _cache_timestamp = time.time()
    return zones


def _generate_mock_weather() -> List[Dict[str, Any]]:
    """Generate mock weather data when API key is not available."""
    import random
    zones = []
    for city, state, lat, lon, crops in AGRICULTURAL_CITIES:
        temp = random.uniform(15, 35)
        humidity = random.uniform(40, 95)
        risk = calculate_risk(temp, humidity)
        zones.append({
            "city": city,
            "state": state,
            "latitude": lat,
            "longitude": lon,
            "crops": crops,
            "temperature": round(temp, 1),
            "humidity": round(humidity, 1),
            "wind_speed": round(random.uniform(1, 15), 1),
            "weather_desc": "mock data",
            "risk": risk,
            "radius_km": 60 if risk == "HIGH" else 40 if risk == "MEDIUM" else 25,
        })
    return zones
