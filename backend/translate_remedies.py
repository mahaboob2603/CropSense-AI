import json
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app/services")))
from remedies import REMEDIES

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# We'll try to find a working key, prioritizing GEMINI_API_KEY_1
key = os.getenv("GEMINI_API_KEY_1") or os.getenv("GEMINI_API_KEY_2") or os.getenv("GEMINI_API_KEY")
genai.configure(api_key=key)

available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
model_name = next((m for m in available_models if 'flash' in m.lower()), available_models[0] if available_models else 'gemini-1.5-flash')
print(f"Using dynamic model: {model_name}")
model = genai.GenerativeModel(model_name)


def translate_data(en_data, target_lang_name, target_lang_code):
    prompt = f"""
Translate the following structured agricultural remedy data into {target_lang_name}.
Return ONLY valid JSON with exactly the same keys: disease_name, crop, cause, symptoms, treatment_steps, organic_options, chemical_options, prevention.
Do not use Markdown blocks (```json). Just the raw JSON. Ensure accurate agricultural terminology in {target_lang_name} ({target_lang_code}).

Data:
{json.dumps(en_data, indent=2)}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error translating to {target_lang_name}:", e)
        return None

new_remedies = {}

# We check if it actually needs translation. If the text in treatment_steps[0] is in English for HI/TE, we translate.
def needs_translation(data, lang_code):
    if lang_code not in data:
        return True
    
    # Check a field to see if it looks like English still
    steps = data[lang_code].get("treatment_steps", [])
    if not steps:
        return True
    
    first_step = steps[0]
    # Simple heuristic: if it contains typical english words or characters from a-zA-Z, it might need translation
    # But some crops have english names. Let's check the length of a-zA-Z characters
    eng_chars = sum(1 for c in first_step if 'a' <= c.lower() <= 'z')
    # If more than 50% of characters are english letters, it's probably not translated
    if eng_chars > len(first_step) * 0.5:
        return True
    return False

total = len(REMEDIES)
count = 0

for disease_name, data in REMEDIES.items():
    count += 1
    print(f"[{count}/{total}] Checking {disease_name}...")
    
    en_data = data.get("EN")
    if not en_data:
        new_remedies[disease_name] = data
        continue
        
    needs_hi = needs_translation(data, "HI")
    needs_te = needs_translation(data, "TE")
    
    if needs_hi:
        print("  Translating to Hindi...")
        hi_data = translate_data(en_data, "Hindi", "HI")
        if hi_data:
            data["HI"] = hi_data
        time.sleep(1) # rate limit prevention

    if needs_te:
        print("  Translating to Telugu...")
        te_data = translate_data(en_data, "Telugu", "TE")
        if te_data:
            data["TE"] = te_data
        time.sleep(1)
        
    new_remedies[disease_name] = data

# Write the result safely
import pprint

dict_str = "REMEDIES = " + json.dumps(new_remedies, ensure_ascii=False, indent=4)

with open("app/services/remedies.py", "w", encoding="utf-8") as f:
    f.write(f"import json\n\n{dict_str}\n\n")
    f.write('''def get_remedy_for_disease(disease_name: str) -> dict:
    """
    Returns the remedy dictionary mapping (EN, HI, TE) for a given disease string.
    If exact match isn't found, falls back to Tomato___healthy or a default.
    """
    if disease_name in REMEDIES:
        return REMEDIES[disease_name]
    
    for d in REMEDIES.keys():
        if d.lower() in disease_name.lower():
            return REMEDIES[d]
            
    return REMEDIES.get("Tomato___healthy")
''')

print("Translation complete and remedies.py updated!")
