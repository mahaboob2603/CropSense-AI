import os
import requests
import google.generativeai as genai

WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_spread_risk(lat: float, lon: float, crop_name: str = "Unknown", disease_name: str = "Unknown") -> dict:
    """
    Fetches real-time weather from OpenWeatherMap and generates an AI insight
    explaining how current conditions affect the specific crop and disease.
    """
    temp = 25.0
    humidity = 60.0
    risk_level = "UNKNOWN"
    
    if WEATHER_API_KEY:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                temp = float(data["main"]["temp"])
                humidity = float(data["main"]["humidity"])
                risk_level = calculate_risk(temp, humidity)
        except Exception as e:
            print(f"Weather API Error: {e}")
            risk_level = "UNKNOWN"
    else:
        # Mock values if no API key
        risk_level = calculate_risk(temp, humidity)
    
    explanation = f"Current temperature is {temp}°C with {humidity}% humidity. These conditions represent a {risk_level} risk for {crop_name} health."

    # Intercept with AI context if Gemini is available
    if GEMINI_API_KEY and risk_level != "UNKNOWN" and "Reject" not in disease_name and disease_name != "Unknown":
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
You are an expert agronomist AI for a dashboard.
A farmer's {crop_name} crop has been diagnosed with '{disease_name}'.
The current live weather at their GPS location is exactly {temp}°C with robust {humidity}% humidity.
Write exactly ONE concise, professional sentence (max 25 words) explaining how these CURRENT real-time weather conditions will affect the spread or severity of this specific disease.
Do not recommend treatments, only atmospheric facts. Do not use Markdown.
"""
            response = model.generate_content(prompt)
            if response.text:
                explanation = response.text.replace('\n', ' ').strip()
        except Exception as e:
            print("Gemini Weather Insight Error:", e)
            
    return {
        "risk_level": risk_level,
        "temperature": temp,
        "humidity": humidity,
        "condition_explanation": explanation
    }

def calculate_risk(temp: float, humidity: float) -> str:
    if humidity > 75 and 18 <= temp <= 28:
        return "HIGH"
    elif humidity > 60 and 15 <= temp <= 32:
        return "MEDIUM"
    else:
        return "LOW"

