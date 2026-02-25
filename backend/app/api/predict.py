import time
import cv2
import traceback
import base64
from io import BytesIO
from PIL import Image as PILImage
from datetime import datetime
import uuid
import os

from fastapi import APIRouter, File, UploadFile, Depends, Form, HTTPException
from sqlalchemy.orm import Session
import numpy as np

from ..db.session import get_db
from ..db.models import Detection, User
from ..core.dependencies import get_current_user
from ..services.weather import get_spread_risk
from ..services.remedies import get_remedy_for_disease

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml_pipeline")))
import tensorflow as tf
from dip_module import apply_production_dip, resize_image

router = APIRouter()

# Global Model Cache
models_cache = {
    "raw": None,
    "dip": None
}

NODIP_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml_pipeline/model_nodip.keras"))
DIP_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml_pipeline/model_with_dip.keras"))

CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

def load_models():
    if models_cache["raw"] is None and os.path.exists(NODIP_MODEL_PATH):
        models_cache["raw"] = tf.keras.models.load_model(NODIP_MODEL_PATH)
    if models_cache["dip"] is None and os.path.exists(DIP_MODEL_PATH):
        models_cache["dip"] = tf.keras.models.load_model(DIP_MODEL_PATH)

def get_class_name(index):
    if 0 <= index < len(CLASS_NAMES):
        return CLASS_NAMES[index]
    return "Unknown"

def determine_severity(confidence):
    if confidence > 0.90: return "Severe"
    if confidence > 0.75: return "Moderate"
    return "Mild"

def _numpy_to_base64_rgb(img_rgb) -> str:
    """Convert an RGB numpy array to a JPEG base64 string."""
    try:
        pil_img = PILImage.fromarray(img_rgb.astype(np.uint8))
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG", quality=85)
        return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        print(f"Base64 error: {e}")
        return ""

def _numpy_to_base64_gray(img_gray) -> str:
    """Convert a grayscale numpy array to a JPEG base64 string."""
    try:
        pil_img = PILImage.fromarray(img_gray.astype(np.uint8), mode="L")
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG", quality=85)
        return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        print(f"Base64 error: {e}")
        return ""


@router.post("/predict")
async def predict_adaptive(
    file: UploadFile = File(...),
    latitude: float = Form(None),
    longitude: float = Form(None),
    force_dip_ui: bool = Form(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Adaptive Dual-Model Inference endpoint.
    1. Loads raw image. Checks brightness/blur.
    2. Suggests DIP if blurry or very poor lighting.
    3. Runs model_nodip. If confidence >= 0.75, accept.
    4. Else, runs optimized DIP pipeline + model_with_dip. Takes the best.
    """
    request_start = time.time()
    temp_file = f"temp_predict_{uuid.uuid4()}.jpg"
    
    try:
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large.")
        with open(temp_file, "wb") as buffer:
            buffer.write(contents)

        load_models()
        raw_model = models_cache["raw"]
        dip_model = models_cache["dip"]
        
        # 1. Read & Basic Checks
        prep_t0 = time.time()
        img_bgr = cv2.imread(temp_file)
        if img_bgr is None:
            raise HTTPException(status_code=400, detail="Invalid image file.")
            
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        blur_variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculate extreme pixels for brightness check
        total_pixels = gray.size
        dark_pixels = np.sum(gray < 40)
        bright_pixels = np.sum(gray > 215)
        perc_dark = (dark_pixels / total_pixels) * 100
        perc_bright = (bright_pixels / total_pixels) * 100
        
        brightness = np.mean(gray) # keep for logging/diagnostics
        
        is_blurry = blur_variance < 100 # Adjust this based on validation dataset percentiles
        is_bad_lighting = perc_dark > 20 or perc_bright > 20
        force_dip = force_dip_ui or is_blurry or is_bad_lighting
        
        # Leaf Validation Stage (OOD Protection)
        # Compute GLI-based green ratio on a small version of the image
        small_img = resize_image(img_bgr, (64, 64))
        b, g, r = cv2.split(small_img)
        g_16 = g.astype(np.int16)
        r_16 = r.astype(np.int16)
        b_16 = b.astype(np.int16)
        exg_small = 2 * g_16 - r_16 - b_16
        green_pixels = np.sum(exg_small > 20)
        green_ratio = green_pixels / (64 * 64)
        
        if green_ratio < 0.15:
            # Graceful OOD Rejection
            return {
                "id": str(uuid.uuid4()),
                "user_id": current_user.id,
                "disease_name": "Non-Leaf Image",
                "confidence": 0.0,
                "latitude": latitude,
                "longitude": longitude,
                "spread_risk": "UNKNOWN",
                "severity": "Unknown",
                "treatment": "Image does not appear to contain a plant leaf. Please upload a clear photo of a leaf.",
                "remedies": None,
                "grad_cam_base64": None,
                "diagnostics": {
                    "inference_mode": "NON_LEAF_REJECT",
                    "green_ratio": round(float(green_ratio), 4),
                    "message": "Image does not appear to contain a plant leaf.",
                    "latency_ms": {
                        "total": round((time.time() - request_start) * 1000, 2)
                    }
                }
            }
        
        from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

        final_disease = "Unknown"
        final_conf = 0.0
        mode = "RAW_CONFIDENT"
        mask_b64 = None
        gli_b64 = None
        lab_b64 = None
        combined_b64 = None
        
        raw_idx = -1
        raw_conf = 0.0
        raw_disease = "Unknown"
        raw_time = 0
        dip_time = 0
        dip_inf_time = 0
        dip_conf = 0.0
        improvement = 0.0
        
        # If models missing, return mock
        if not raw_model or not dip_model:
            final_disease = "Tomato___Early_blight"
            final_conf = 0.92
            mode = "MOCK MODE (MODELS NOT FOUND)"
            raw_conf = 0.85
        else:
            # 2. Raw Inference
            img_rgb_raw = resize_image(img_bgr, size=(224, 224))
            img_rgb_raw = cv2.cvtColor(img_rgb_raw, cv2.COLOR_BGR2RGB)
            raw_input = preprocess_input(img_rgb_raw.astype(np.float32))
            raw_batch = np.expand_dims(raw_input, axis=0)
            
            inf_t0 = time.time()
            raw_preds = raw_model.predict(raw_batch, verbose=0)[0]
            raw_time = (time.time() - inf_t0) * 1000
            
            raw_idx = np.argmax(raw_preds)
            raw_conf = float(raw_preds[raw_idx])
            raw_disease = get_class_name(raw_idx)
            
            final_disease = raw_disease
            final_conf = raw_conf
            
            # 3. Decision Logic -> Trigger DIP if needed
            if force_dip or raw_conf < 0.75:
                # Run highly-optimized DIP
                segmented_rgb, final_mask, dip_prep_time, intermediate_masks = apply_production_dip(img_bgr)
                dip_time = dip_prep_time
                
                dip_input = preprocess_input(segmented_rgb.astype(np.float32))
                dip_batch = np.expand_dims(dip_input, axis=0)
                
                inf_t1 = time.time()
                dip_preds = dip_model.predict(dip_batch, verbose=0)[0]
                dip_inf_time = (time.time() - inf_t1) * 1000
                
                dip_idx = np.argmax(dip_preds)
                dip_conf = float(dip_preds[dip_idx])
                dip_disease = get_class_name(dip_idx)
                
                improvement = dip_conf - raw_conf
                
                if dip_conf > raw_conf + 0.10:
                    final_disease = dip_disease
                    final_conf = dip_conf
                    mode = "DIP_RECOVERY"
                    mask_b64 = _numpy_to_base64_rgb(segmented_rgb)
                    gli_b64 = _numpy_to_base64_gray(intermediate_masks["gli"])
                    lab_b64 = _numpy_to_base64_gray(intermediate_masks["lab"])
                    combined_b64 = _numpy_to_base64_gray(intermediate_masks["combined"])
                elif dip_conf > raw_conf:
                    final_disease = dip_disease
                    final_conf = dip_conf
                    mode = "MINOR_IMPROVEMENT"
                    mask_b64 = _numpy_to_base64_rgb(segmented_rgb)
                else:
                    mode = "RAW_BETTER" # Keep raw

            # Case D: Both low confidence
            if final_conf < 0.55:
                mode = "LOW_CONFIDENCE_REJECT"
                
        prep_time = (time.time() - prep_t0) * 1000

        # Create DB record (if not rejected)
        risk = "UNKNOWN"
        weather_insights = {
            "risk_level": "UNKNOWN",
            "temperature": 0.0,
            "humidity": 0.0,
            "condition_explanation": "Weather data unavailable."
        }
        if latitude is not None and longitude is not None:
            crop_name = final_disease.split("___")[0].replace("_", " ") if "___" in final_disease else "Plant"
            weather_insights = get_spread_risk(latitude, longitude, crop_name, final_disease)
            risk = weather_insights.get("risk_level", "UNKNOWN")
            
        severity = determine_severity(final_conf)
        
        # Override values if low confidence reject
        if mode == "LOW_CONFIDENCE_REJECT":
            final_disease = "Low Confidence"
            treatment_text = "Image quality too low for reliable diagnosis. Please retake photo with better lighting and focus."
            remedy_data = None
            detection_id = str(uuid.uuid4())
        else:
            detection = Detection(
                user_id=current_user.id,
                disease_name=final_disease,
                confidence=final_conf,
                latitude=latitude,
                longitude=longitude,
                spread_risk=risk,
                severity=severity,
                timestamp=datetime.utcnow()
            )
            db.add(detection)
            db.commit()
            db.refresh(detection)
            detection_id = detection.id
            remedy_data = get_remedy_for_disease(detection.disease_name)
            treatment_text = " ".join(remedy_data["EN"]["treatment_steps"])
        
        try:
            total_latency = (time.time() - request_start) * 1000

            return {
                "id": detection_id,
                "user_id": current_user.id,
                "disease_name": final_disease,
                "confidence": final_conf,
                "latitude": latitude,
                "longitude": longitude,
                "spread_risk": risk,
                "severity": severity,
                "treatment": treatment_text,
                "remedies": remedy_data,
                "weather_insights": weather_insights,
                "grad_cam_base64": "MOCKED_BASE64_FOR_DEMO",
                # New Diagnostic Meta
                "diagnostics": {
                    "inference_mode": mode,
                    "blur_variance": round(float(blur_variance), 2),
                    "brightness": round(float(brightness), 2),
                    "green_ratio": round(float(green_ratio), 4),
                    "raw_confidence": round(float(raw_conf), 4),
                    "dip_confidence": round(float(dip_conf), 4),
                    "improvement_percent": round(float(improvement) * 100, 2),
                    "mask_preview_base64": mask_b64,
                    "gli_mask_base64": gli_b64,
                    "lab_mask_base64": lab_b64,
                    "combined_mask_base64": combined_b64,
                    "latency_ms": {
                        "preprocessing": round(float(prep_time), 2),
                        "raw_inference": round(float(raw_time), 2),
                        "dip_preprocessing": round(float(dip_time), 2),
                        "dip_inference": round(float(dip_inf_time), 2),
                        "total": round(float(total_latency), 2)
                    }
                }
            }
        except Exception as inner_e:
            with open("error_log.txt", "w") as f:
                import traceback
                f.write(traceback.format_exc())
            raise inner_e
            
    except HTTPException:
        raise
    except Exception as e:
        with open("error_log.txt", "w") as f:
            import traceback
            f.write(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@router.post("/predict-compare")
async def predict_compare_legacy(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    Legacy endpoint for Technical Analysis tab to show DIP stages.
    We return dummy stages rather than running KMeans/GrabCut in production.
    """
    from fastapi import Response
    # In a fully refactored app, this endpoint might be removed or placed behind a 'debug' flag.
    # For now, return mock data to keep the frontend Technical Analysis tab from breaking.
    return {
        "raw": {"disease_name": "Unknown", "confidence": 0.0},
        "dip": {"disease_name": "Unknown", "confidence": 0.0},
        "stages": [],
        "improvement": 0.0
    }
