from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import DBSCAN
from ..db.session import get_db
from ..db.models import Detection
from ..services.live_weather import fetch_weather_for_cities

router = APIRouter()

# ── Curated Indian Crop Disease Hotspots (ICAR-based) ──────────────────────
# Real well-known disease-prone regions across India
DISEASE_HOTSPOTS = [
    # Apple Belt — Himalayan Region
    {
        "id": "hs_shimla_scab", "latitude": 31.1048, "longitude": 77.1734,
        "disease": "Apple___Apple_scab", "region": "Shimla, HP",
        "severity": "HIGH", "note": "Endemic scab zone — cool humid orchards at 2000m elevation",
        "season": "Apr–Sep", "crop": "Apple",
    },
    {
        "id": "hs_kullu_rust", "latitude": 31.9579, "longitude": 77.1095,
        "disease": "Apple___Cedar_apple_rust", "region": "Kullu Valley, HP",
        "severity": "MEDIUM", "note": "Juniper-Apple proximity enables rust cycle",
        "season": "May–Aug", "crop": "Apple",
    },
    {
        "id": "hs_srinagar_scab", "latitude": 34.0837, "longitude": 74.7973,
        "disease": "Apple___Apple_scab", "region": "Srinagar, J&K",
        "severity": "HIGH", "note": "Kashmir's high-humidity orchards — persistent scab pressure",
        "season": "Apr–Oct", "crop": "Apple",
    },
    {
        "id": "hs_srinagar_blackrot", "latitude": 34.15, "longitude": 74.85,
        "disease": "Apple___Black_rot", "region": "Baramulla, J&K",
        "severity": "MEDIUM", "note": "Post-harvest fruit rot in storage — warm humid conditions",
        "season": "Jul–Sep", "crop": "Apple",
    },

    # Tomato Belt — Central & South India
    {
        "id": "hs_nashik_blight", "latitude": 19.9975, "longitude": 73.7898,
        "disease": "Tomato___Late_blight", "region": "Nashik, MH",
        "severity": "HIGH", "note": "India's tomato capital — monsoon blight outbreaks regular",
        "season": "Jun–Oct", "crop": "Tomato",
    },
    {
        "id": "hs_pune_earlyblight", "latitude": 18.5204, "longitude": 73.8567,
        "disease": "Tomato___Early_blight", "region": "Pune, MH",
        "severity": "MEDIUM", "note": "Alternaria solani persists in warm humid kharif season",
        "season": "Jul–Nov", "crop": "Tomato",
    },
    {
        "id": "hs_kurnool_bacterial", "latitude": 15.8281, "longitude": 78.0373,
        "disease": "Tomato___Bacterial_spot", "region": "Kurnool, AP",
        "severity": "HIGH", "note": "Xanthomonas outbreaks in rainfed tomato fields",
        "season": "Jun–Sep", "crop": "Tomato",
    },
    {
        "id": "hs_guntur_bacterial", "latitude": 16.3067, "longitude": 80.4365,
        "disease": "Tomato___Bacterial_spot", "region": "Guntur, AP",
        "severity": "MEDIUM", "note": "Warm season bacterial infections in chili and tomato",
        "season": "Jul–Oct", "crop": "Tomato/Chili",
    },
    {
        "id": "hs_bangalore_leafmold", "latitude": 12.9716, "longitude": 77.5946,
        "disease": "Tomato___Leaf_Mold", "region": "Bangalore Rural, KA",
        "severity": "MEDIUM", "note": "Greenhouse and polyhouse tomato leaf mold",
        "season": "Year-round", "crop": "Tomato",
    },
    {
        "id": "hs_coimbatore_yellowcurl", "latitude": 11.0168, "longitude": 76.9558,
        "disease": "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "region": "Coimbatore, TN",
        "severity": "HIGH", "note": "Whitefly-transmitted TYLCV — warm irrigated regions",
        "season": "Feb–May", "crop": "Tomato",
    },

    # Potato Belt — North India
    {
        "id": "hs_agra_lateblight", "latitude": 27.1767, "longitude": 78.0081,
        "disease": "Potato___Late_blight", "region": "Agra, UP",
        "severity": "HIGH", "note": "Phytophthora infestans epidemic zone — Indo-Gangetic plains",
        "season": "Nov–Feb", "crop": "Potato",
    },
    {
        "id": "hs_patna_lateblight", "latitude": 25.6093, "longitude": 85.1376,
        "disease": "Potato___Late_blight", "region": "Patna, BH",
        "severity": "MEDIUM", "note": "Bihar potato belt — winter fog creates late blight conditions",
        "season": "Dec–Feb", "crop": "Potato",
    },

    # Grape Belt — Western India
    {
        "id": "hs_sangli_blackrot", "latitude": 16.8524, "longitude": 74.5815,
        "disease": "Grape___Black_rot", "region": "Sangli, MH",
        "severity": "HIGH", "note": "Major grape export zone — black rot in monsoon",
        "season": "Jun–Sep", "crop": "Grape",
    },
    {
        "id": "hs_nashik_grapeesca", "latitude": 20.05, "longitude": 73.82,
        "disease": "Grape___Esca_(Black_Measles)", "region": "Nashik Vineyards, MH",
        "severity": "MEDIUM", "note": "Trunk disease in older vineyards — reduced yield",
        "season": "Mar–Jun", "crop": "Grape",
    },

    # Corn/Maize Belt
    {
        "id": "hs_karnal_cornrust", "latitude": 29.6857, "longitude": 76.9905,
        "disease": "Corn_(maize)___Common_rust_", "region": "Karnal, HR",
        "severity": "MEDIUM", "note": "Puccinia sorghi in kharif maize — warm humid zone",
        "season": "Jul–Oct", "crop": "Corn",
    },
    {
        "id": "hs_indore_cornblight", "latitude": 22.7196, "longitude": 75.8577,
        "disease": "Corn_(maize)___Northern_Leaf_Blight", "region": "Indore, MP",
        "severity": "MEDIUM", "note": "Exserohilum turcicum — central India maize",
        "season": "Jul–Sep", "crop": "Corn",
    },

    # Rice Belt — East & South India
    {
        "id": "hs_cuttack_riceblast", "latitude": 20.4625, "longitude": 85.8830,
        "disease": "Rice___Leaf_Blast", "region": "Cuttack, OD",
        "severity": "HIGH", "note": "NRRI headquarters — endemic blast zone",
        "season": "Jul–Nov", "crop": "Rice",
    },
    {
        "id": "hs_thanjavur_ricebrown", "latitude": 10.7870, "longitude": 79.1378,
        "disease": "Rice___Brown_Spot", "region": "Thanjavur, TN",
        "severity": "MEDIUM", "note": "Cauvery delta — brown spot in nitrogen-deficient paddies",
        "season": "Sep–Jan", "crop": "Rice",
    },

    # Pepper/Chili Belt — Andhra Pradesh & Karnataka
    {
        "id": "hs_guntur_pepperbact", "latitude": 16.3067, "longitude": 80.4365,
        "disease": "Pepper,_bell___Bacterial_spot", "region": "Guntur, AP",
        "severity": "HIGH", "note": "India's chili capital — Xanthomonas in warm rains",
        "season": "Jul–Oct", "crop": "Pepper",
    },
    {
        "id": "hs_dharwad_pepperbact", "latitude": 15.4589, "longitude": 75.0078,
        "disease": "Pepper,_bell___Bacterial_spot", "region": "Dharwad, KA",
        "severity": "MEDIUM", "note": "North Karnataka capsicum — bacterial spot in monsoon",
        "season": "Jun–Sep", "crop": "Pepper",
    },

    # Citrus Belt — Nagpur & Vidarbha
    {
        "id": "hs_nagpur_greening", "latitude": 21.1458, "longitude": 79.0882,
        "disease": "Orange___Haunglongbing_(Citrus_greening)", "region": "Nagpur, MH",
        "severity": "HIGH", "note": "India's Orange City — HLB via psyllid vector spreading",
        "season": "Year-round", "crop": "Orange",
    },
    {
        "id": "hs_coorg_citrus", "latitude": 12.4244, "longitude": 75.7382,
        "disease": "Orange___Haunglongbing_(Citrus_greening)", "region": "Coorg, KA",
        "severity": "MEDIUM", "note": "Coorg mandarin oranges — citrus greening threat",
        "season": "Year-round", "crop": "Orange",
    },

    # Strawberry — Mahabaleshwar & Nilgiris
    {
        "id": "hs_mahabaleshwar_strawberry", "latitude": 17.9237, "longitude": 73.6586,
        "disease": "Strawberry___Leaf_scorch", "region": "Mahabaleshwar, MH",
        "severity": "MEDIUM", "note": "Hill station strawberry farms — leaf scorch in monsoon",
        "season": "Jun–Sep", "crop": "Strawberry",
    },

    # Squash/Cucurbit Belt
    {
        "id": "hs_lucknow_squash", "latitude": 26.8467, "longitude": 80.9462,
        "disease": "Squash___Powdery_mildew", "region": "Lucknow, UP",
        "severity": "MEDIUM", "note": "Cucurbit powdery mildew in warm, dry post-monsoon",
        "season": "Sep–Nov", "crop": "Squash",
    },
]


# ── Existing Endpoint (backward compat) ───────────────────────────────────
@router.get("/heatmap-data", response_model=List[Dict[str, Any]])
async def get_heatmap_data(db: Session = Depends(get_db)):
    return _get_user_detections(db)


# ── New 3-Layer Live Endpoint ─────────────────────────────────────────────
@router.get("/heatmap-live")
async def get_heatmap_live(db: Session = Depends(get_db)):
    """
    Returns 3 layers for the outbreak heatmap:
    1. weather_zones — real-time weather-based risk areas
    2. disease_hotspots — curated ICAR-based known hotspots
    3. user_detections — DBSCAN-clustered user uploads
    """
    weather_zones = fetch_weather_for_cities()
    user_detections = _get_user_detections(db)

    return {
        "weather_zones": weather_zones,
        "disease_hotspots": DISEASE_HOTSPOTS,
        "user_detections": user_detections,
    }


def _get_user_detections(db: Session) -> List[Dict[str, Any]]:
    """Existing DBSCAN logic for user-uploaded detections."""
    detections = db.query(Detection).filter(
        Detection.latitude != None, Detection.longitude != None
    ).all()

    if not detections:
        return []

    coords = np.array([[d.latitude, d.longitude] for d in detections])
    coords_radians = np.radians(coords)

    EARTH_RADIUS = 6371.0
    eps_km = 50.0
    eps_radians = eps_km / EARTH_RADIUS

    dbscan = DBSCAN(eps=eps_radians, min_samples=3, metric='haversine', algorithm='ball_tree')
    clusters = dbscan.fit_predict(coords_radians)

    result = []

    # Noise points as isolated markers
    for idx, cluster_id in enumerate(clusters):
        if cluster_id == -1:
            d = detections[idx]
            result.append({
                "type": "point",
                "id": str(d.id),
                "latitude": d.latitude,
                "longitude": d.longitude,
                "disease_name": d.disease_name,
                "spread_risk": d.spread_risk,
                "confidence": d.confidence,
                "point_count": 1
            })

    # Outbreak clusters
    unique_clusters = set(clusters) - {-1}
    for cluster_id in unique_clusters:
        indices = np.where(clusters == cluster_id)[0]
        cluster_coords = coords[indices]

        centroid_lat = np.mean(cluster_coords[:, 0])
        centroid_lon = np.mean(cluster_coords[:, 1])

        risks = [detections[i].spread_risk for i in indices]
        risk_counts = {r: risks.count(r) for r in set(risks)}
        dominant_risk = max(risk_counts, key=risk_counts.get)

        diseases = [detections[i].disease_name for i in indices]
        disease_counts = {d: diseases.count(d) for d in set(diseases)}
        dominant_disease = max(disease_counts, key=disease_counts.get)

        avg_conf = np.mean([detections[i].confidence for i in indices])

        result.append({
            "type": "cluster",
            "id": f"cluster_{cluster_id}",
            "latitude": centroid_lat,
            "longitude": centroid_lon,
            "disease_name": dominant_disease,
            "spread_risk": dominant_risk,
            "confidence": float(avg_conf),
            "point_count": len(indices)
        })

    return result
