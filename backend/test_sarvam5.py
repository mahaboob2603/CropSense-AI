import requests
url = 'https://api.sarvam.ai/text-to-speech'
payload = {'inputs': ['नमस्ते दुनिया'], 'target_language_code': 'hi-IN', 'speaker': 'anushka', 'pace': 1.0, 'speech_sample_rate': 8000, 'enable_preprocessing': True, 'model': 'bulbul:v3'}
headers = {'api-subscription-key': 'sk_uyegyudu_YMmGb5oIG1vycJB8DbeKH8M2', 'Content-Type': 'application/json'}
res = requests.post(url, json=payload, headers=headers)
print(res.status_code)
