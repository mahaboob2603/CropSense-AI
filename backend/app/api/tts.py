import os
import requests
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ..core.dependencies import get_current_user
from ..db.models import User

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    lang: str = "EN" # Expected: HI or TE (EN handled by browser)

class TTSResponse(BaseModel):
    audio_base64: str

# Sarvam AI Language Codes Mapping
# Maps our standard app language codes to Sarvam's expected codes
SARVAM_LANG_MAP = {
    "HI": "hi-IN",
    "TE": "te-IN"
}

@router.post("/tts", response_model=TTSResponse)
async def generate_speech(request: TTSRequest, current_user: User = Depends(get_current_user)):
    """
    Generate Text-to-Speech using Sarvam AI for Hindi and Telugu.
    English is typically handled natively on the frontend, but we route it here just in case.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
        
    lang = request.lang.upper()
    api_key = os.getenv("SARVAM_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="SARVAM_API_KEY is not configured on the server")
        
    sarvam_lang = SARVAM_LANG_MAP.get(lang)
    if not sarvam_lang:
        raise HTTPException(status_code=400, detail=f"Language '{lang}' is not supported by this TTS endpoint. Supported: HI, TE")

    url = "https://api.sarvam.ai/text-to-speech"
    
    payload = {
        "inputs": [request.text.strip()],
        "target_language_code": sarvam_lang,
        "speaker": "priya", # Female Indian voice
        "pace": 1.0,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v3"
    }
    
    headers = {
        "api-subscription-key": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Sarvam API returns a list of audios corresponding to the inputs list
        audios = data.get("audios", [])
        if not audios:
            raise HTTPException(status_code=500, detail="Sarvam API returned an empty audio list")
            
        base64_audio = audios[0]
        return TTSResponse(audio_base64=base64_audio)
        
    except requests.exceptions.RequestException as e:
        print("Sarvam API Request Error:", e)
        # Attempt to get more detail from response if available
        error_msg = str(e)
        if hasattr(e, 'response') and e.response:
            try:
                error_msg = e.response.json()
            except:
                error_msg = e.response.text
        print("Sarvam API Error Details:", error_msg)
        raise HTTPException(status_code=502, detail="Failed to synthesize speech via Sarvam AI")
    except Exception as e:
        print("Unexpected error in TTS generation:", e)
        raise HTTPException(status_code=500, detail="Internal server error during speech generation")


# ── Speech-to-Text via Sarvam AI ───────────────────────────────────────────

class STTRequest(BaseModel):
    audio_base64: str  # base64 encoded audio (webm from browser)
    lang: str = "EN"

class STTResponse(BaseModel):
    transcript: str

SARVAM_STT_LANG_MAP = {
    "EN": "en-IN",
    "HI": "hi-IN",
    "TE": "te-IN",
}

@router.post("/stt", response_model=STTResponse)
async def speech_to_text(request: STTRequest, current_user: User = Depends(get_current_user)):
    """Convert speech audio to text using Sarvam AI."""
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="SARVAM_API_KEY is not configured")

    sarvam_lang = SARVAM_STT_LANG_MAP.get(request.lang.upper(), "en-IN")

    import base64
    import tempfile
    try:
        audio_bytes = base64.b64decode(request.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio data")

    # Save the raw browser audio (WebM format)
    webm_path = None
    wav_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            tmp.write(audio_bytes)
            webm_path = tmp.name

        # Convert WebM → WAV (16kHz mono) using pydub + ffmpeg
        wav_path = webm_path.replace(".webm", ".wav")
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(webm_path, format="webm")
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            audio.export(wav_path, format="wav")
            print(f"STT: Converted WebM ({len(audio_bytes)}B) → WAV ({os.path.getsize(wav_path)}B), duration={len(audio)}ms")
        except Exception as conv_err:
            print(f"STT: WebM→WAV conversion failed: {conv_err}, trying raw upload")
            wav_path = webm_path  # fallback: send as-is

        url = "https://api.sarvam.ai/speech-to-text"
        headers = {"api-subscription-key": api_key}

        with open(wav_path, "rb") as audio_file:
            files = {"file": ("audio.wav", audio_file, "audio/wav")}
            data = {
                "language_code": sarvam_lang,
                "model": "saarika:v2.5",
                "with_timestamps": "false",
            }
            response = requests.post(url, headers=headers, files=files, data=data, timeout=30)

        print(f"STT: Sarvam response status={response.status_code}")
        response.raise_for_status()
        result = response.json()

        transcript = result.get("transcript", "")

        print(f"STT: Transcript = '{transcript}'")
        return STTResponse(transcript=transcript if transcript else "")

    except requests.exceptions.RequestException as e:
        print("Sarvam STT Error:", e)
        error_detail = str(e)
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = e.response.json()
            except Exception:
                error_detail = e.response.text
        print("Sarvam STT Error Details:", error_detail)
        raise HTTPException(status_code=502, detail="Speech-to-text failed via Sarvam AI")
    finally:
        for p in [webm_path, wav_path]:
            if p:
                try:
                    os.unlink(p)
                except Exception:
                    pass
