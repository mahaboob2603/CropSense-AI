from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import os
import google.generativeai as genai
from ..services.remedies import get_remedy_for_disease
from ..core.dependencies import get_current_user
from ..db.models import User

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    disease_context: str
    lang: str = "EN" # EN, HI, TE

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """
    Context-aware Q&A based on the current detected disease using Gemini over the local JSON database.
    """
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    lang = request.lang.upper() if request.lang else "EN"
    if lang not in ["EN", "HI", "TE"]:
        lang = "EN"
        
    remedy_data = get_remedy_for_disease(request.disease_context)
    if not remedy_data or lang not in remedy_data:
        raise HTTPException(status_code=404, detail="Disease context not found")
        
    structured_data = remedy_data[lang]
    
    keys = [
        os.getenv("GEMINI_API_KEY_1"),
        os.getenv("GEMINI_API_KEY_2"),
        os.getenv("GEMINI_API_KEY") # Legacy fallback
    ]
    api_keys = [k for k in keys if k]
    
    if api_keys:
        import logging
        
        prompt = f"""
You are CropSense AI, a helpful agricultural assistant. The user's plant is currently diagnosed with '{structured_data['disease_name']}'. 
Here is all the reliable remedy data we have for this disease:
{structured_data}

The user is asking this question: "{question}"
Answer their question directly and concisely. You can use the provided remedy data as a starting point.
CRITICAL RULE 1: The user might type their query in transliterated English (Hinglish/Tanglish). You MUST reply STRICTLY in the native script of this language code: {lang} (English for EN, Devanagari for HI, Telugu script for TE). DO NOT reply in English characters unless the language code is EN.
CRITICAL RULE 2: Your response WILL be spoken by a Voice Assistant via Text-to-Speech. You MUST keep your answer extremely short, conversational, and UNDER 300 characters (approx 2 sentences). Do not use lists, bullet points, or markdown. Do not mention you are an AI.
If the question is completely unrelated to agriculture or the plant, politely decline to answer.
"""
        
        gemini_models_to_try = [
            'gemini-1.5-flash',
            'gemini-1.5-flash-8b',
            'gemini-pro'
        ]
        
        for api_key in api_keys:
            genai.configure(api_key=api_key)
            for model_name in gemini_models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    return ChatResponse(answer=response.text.strip())
                except Exception as e:
                    logging.error(f"Gemini API Error with key {api_key[:8]}... using model {model_name}: {str(e)}")
                    # If it's a 429 or other exhaustion error, break inner loop to try next key
                    if "429" in str(e) or "quota" in str(e).lower():
                        break
                    continue
                
        # If we reach here, ALL keys and models failed. Fall down to manual handlers below.
            
    # --- Intelligent Contextual Fallback (If no API Key or API fails) ---
    question_lower = question.lower()
    
    fallbacks = {
        "EN": "I'm a bit restricted right now. Please refer to my detailed treatment text on the screen.",
        "HI": "मैं अभी थोड़ा सीमित हूं। कृपया स्क्रीन पर मेरा विस्तृत उपचार टेक्स्ट देखें।",
        "TE": "నేను ప్రస్తుతం కొంచెం పరిమితంగా ఉన్నాను. దయచేసి స్క్రీన్‌పై ఉన్న నా సవివరమైన చికిత్స టెక్స్ట్‌ని చూడండి."
    }
    answer = fallbacks.get(lang, fallbacks["EN"])
    
    # Very simple keyword fallback routing if Gemini isn't available
    if any(k in question_lower for k in ["organic", "natural", "home", "जैविक", "घर", "ఆర్గానిక్", "సేంద్రీయ", "jaivik", "ghar", "sendriya", "prakruthi"]):
        if structured_data.get("organic_options"):
            if lang == "EN": answer = "For organic options, try: " + ". ".join(structured_data["organic_options"])
            if lang == "HI": answer = "जैविक उपचार: " + ". ".join(structured_data["organic_options"])
            if lang == "TE": answer = "సేంద్రియ పద్ధతులు: " + ". ".join(structured_data["organic_options"])
    elif any(k in question_lower for k in ["chemical", "spray", "medicine", "fungicide", "रसायन", "दवा", "కెమికల్", "మందు", "rasayan", "dawa", "k রাস", "mandu", "rasayana"]):
        if structured_data.get("chemical_options"):
            if lang == "EN": answer = "Chemical treatments: " + ". ".join(structured_data["chemical_options"])
            if lang == "HI": answer = "रासायनिक उपचार: " + ". ".join(structured_data["chemical_options"])
            if lang == "TE": answer = "రసాయన స్థితులు: " + ". ".join(structured_data["chemical_options"])
    elif any(k in question_lower for k in ["prevent", "avoid", "future", "roktham", "रोकथाम", "నివారణ", "nivarana", "aputha"]):
        if structured_data.get("prevention"):
            if lang == "EN": answer = "Prevention steps: " + ". ".join(structured_data["prevention"])
            if lang == "HI": answer = "रोकथाम के उपाय: " + ". ".join(structured_data["prevention"])
            if lang == "TE": answer = "నివారణ చర్యలు: " + ". ".join(structured_data["prevention"])
    elif any(k in question_lower for k in ["cause", "why", "reason", "कारण", "ఎందుకు", "కారణం", "karan", "enduku", "karana"]):
        if structured_data.get("cause"):
            answer = structured_data["cause"]
    elif any(k in question_lower for k in ["symptom", "sign", "look", "लक्षण", "లక్షణాలు", "lakshan", "lakshanalu"]):
        if structured_data.get("symptoms"):
            answer = ". ".join(structured_data["symptoms"])
    elif any(k in question_lower for k in ["step", "do", "how", "चरण", "ఎలా", "what", "charan", "ela"]):
        if structured_data.get("treatment_steps"):
            answer = ". ".join(structured_data["treatment_steps"])

    return ChatResponse(answer=answer)
