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
CRITICAL INSTRUCTION: You MUST translate every single English word in the values into {target_lang_name} ({target_lang_code}). 
Do NOT leave any English text in the arrays for symptoms, treatment_steps, organic_options, chemical_options, or prevention. Translate them completely into {target_lang_name} script.
Return ONLY valid JSON with exactly the same keys: disease_name, crop, cause, symptoms, treatment_steps, organic_options, chemical_options, prevention. Do NOT wrap in ```json.

Data to translate to {target_lang_name}:
{json.dumps(en_data, indent=2)}
"""
    retries = 3
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(text)
            return parsed
        except Exception as e:
            err_msg = str(e)
            print(f"Error on attempt {attempt+1} for {target_lang_name}: {err_msg[:100]}...")
            if "quota" in err_msg.lower() or "429" in err_msg or "exhausted" in err_msg.lower():
                print("Rate limited! Sleeping for 60 seconds...")
                time.sleep(60)
            else:
                time.sleep(5)
    print(f"Failed to translate to {target_lang_name} after {retries} attempts.")
    return None

new_remedies = {}

def needs_translation(data, lang_code):
    if lang_code not in data:
        return True
    
    # Check if a text field contains mostly English characters
    steps = data[lang_code].get("treatment_steps", [])
    if not steps:
        return True
    
    first_step = steps[0]
    eng_chars = sum(1 for c in first_step if 'a' <= c.lower() <= 'z')
    # If more than 25% of characters are english letters in a localized string, it's a fake translation
    if eng_chars > len(first_step) * 0.25:
        return True
    return False

total = len(REMEDIES)
count = 0

def save_progress():
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
            if "treatment_steps" in hi_data and hi_data["treatment_steps"]:
                print(f"    Sample: {hi_data['treatment_steps'][0][:50]}...")
        time.sleep(5) # rate limit prevention

    if needs_te:
        print("  Translating to Telugu...")
        te_data = translate_data(en_data, "Telugu", "TE")
        if te_data:
            data["TE"] = te_data
            if "treatment_steps" in te_data and te_data["treatment_steps"]:
                print(f"    Sample: {te_data['treatment_steps'][0][:50]}...")
        time.sleep(5)
        
    new_remedies[disease_name] = data
    save_progress() # incremental save!

print("Translation complete and remedies.py updated!")
