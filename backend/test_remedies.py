from app.services.remedies import get_remedy_for_disease
import json

apple_healthy = get_remedy_for_disease("Apple___healthy")
tomato_bacterial = get_remedy_for_disease("Tomato___Bacterial_spot")
unknown = get_remedy_for_disease("Corn___Unknown_disease")

print("APPLE HEALTHY:")
print(json.dumps(apple_healthy["EN"], indent=2))
print("\nTOMATO BACTERIAL:")
print(json.dumps(tomato_bacterial["EN"]["treatment_steps"], indent=2))
print("\nUNKNOWN FALLBACK:")
print(json.dumps(unknown["EN"]["organic_options"], indent=2))
