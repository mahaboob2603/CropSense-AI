import requests
url = 'https://api.sarvam.ai/text-to-speech'
payload = {'inputs': ['नमस्ते दुनिया'], 'target_language_code': 'hi-IN', 'speaker': 'meera', 'pitch': 0, 'pace': 1.0, 'loudness': 1.5, 'speech_sample_rate': 8000, 'enable_preprocessing': True, 'model': 'bulbul:v1'}
headers = {'api-subscription-key': 'sk_uyegyudu_YMmGb5oIG1vycJB8DbeKH8M2', 'Content-Type': 'application/json'}
try:
    res = requests.post(url, json=payload, headers=headers)
    print(res.json()['error']['message'])
except Exception as e:
    print(e)
