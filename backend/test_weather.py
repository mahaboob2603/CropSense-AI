import os
from dotenv import load_dotenv

load_dotenv()

from app.services.weather import get_spread_risk, WEATHER_API_KEY

print(f"API KEY from module: {WEATHER_API_KEY}")

risk = get_spread_risk(17.3850, 78.4867) # Hyderabad coords
print(f"Calculated Risk: {risk}")
