import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend/app/services")))
from remedies import REMEDIES

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("backend/.env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')

def translate_to_telugu(en_data):
    prompt = f"""
Translate the following structured agricultural remedy data into Telugu.
Return ONLY valid JSON with exactly the same keys. Do not use Markdown blocks (```json). Just the raw JSON.
Ensure accurate agricultural terminology in Telugu.

Data:
{json.dumps(en_data, indent=2)}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        telugu_data = json.loads(text)
        return telugu_data
    except Exception as e:
        print("Error translating:", e)
        return None

new_remedies = {}
for disease_name, data in REMEDIES.items():
    if "TE" not in data:
        print(f"Translating {disease_name}...")
        te_data = translate_to_telugu(data["EN"])
        if te_data:
            data["TE"] = te_data
        else:
            print(f"Failed to translate {disease_name}")
    new_remedies[disease_name] = data

# Write just the dictionary part to a string
dict_str = "REMEDIES = " + json.dumps(new_remedies, ensure_ascii=False, indent=4)

# Now read the original remedies.py
with open("backend/app/services/remedies.py", "r", encoding="utf-8") as f:
    original_code = f.read()

# We know the function starts at `def get_remedy_for_disease`
func_start = original_code.find("def get_remedy_for_disease")

# Keep the imports at the top
header = "import json\n\n"

if func_start != -1:
    footer = original_code[func_start:]
else:
    print("Warning: could not find get_remedy_for_disease")
    footer = ""

# Reconstruct
final_code = header + dict_str + "\n\n" + footer

with open("backend/app/services/remedies.py", "w", encoding="utf-8") as f:
    f.write(final_code)

print("Safely injected TE translations and preserved the function!")
