import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

keys = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY")
]
api_keys = [k for k in keys if k]

for api_key in api_keys:
    print(f"Testing Key: {api_key[:8]}...")
    genai.configure(api_key=api_key)
    try:
        print("Available models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        
        # Try a simple generation with the first available model
        model_name = 'models/gemini-1.5-flash'
        print(f"Attempting generation with {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi")
        print(f"Success! Response: {response.text.strip()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    print("-" * 20)
