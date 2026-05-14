"""
Krishikarm v7 — FastAPI Backend Server
Main entry point for the Village Kiosk AI System.
"""

import os
import io
import base64
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path
import secrets
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Local modules
import farmer_db
import face_engine
import voice_engine
import llm_engine
import scheme_matcher
import satellite_advisor
import telemetry_db

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger("kisan-eye")

# FastAPI app
app = FastAPI(
    title="Krishikarm v7 — AI Farming Intelligence",
    description="AI-powered farm advisory system for Indian village panchayats",
    version="6.0.0"
)

# Secure CORS policy
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- AUTHENTICATION DEPENDENCY ---

async def get_current_farmer(
    authorization: str = Header(None),
    x_farmer_id: str = Header(None)
):
    if not authorization or not x_farmer_id:
        raise HTTPException(401, "Missing authorization credentials")
    
    token = authorization.replace("Bearer ", "")
    try:
        f_id = int(x_farmer_id)
    except ValueError:
        raise HTTPException(400, "Invalid Farmer ID format")

    if not farmer_db.verify_token(f_id, token):
        logger.warning(f"⚠️ Auth failure for Farmer ID: {f_id}")
        raise HTTPException(401, "Invalid or expired token")
    
    farmer = farmer_db.get_farmer(f_id)
    if not farmer:
        raise HTTPException(404, "Farmer not found")
    return farmer


# ===== MODELS =====

class FarmerRegister(BaseModel):
    name: str
    village: str
    district: str = ""
    state: str = ""
    language: str = "hi"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    land_acres: float = 0
    crops: list = []
    phone: Optional[str] = None
    father_name: Optional[str] = None
    irrigation_type: Optional[str] = None
    family_members: int = 4
    bpl_card: bool = False
    financial_state: str = "stable"
    annual_income: float = 0
    debt_amount: float = 0

class ChatRequest(BaseModel):
    farmer_id: int
    query: str
    language: str = "hi"

class TelemetryPayload(BaseModel):
    node_id: str
    timestamp: float
    lat: float
    lng: float
    temp: float
    humidity: float
    soil_moisture: float
    ph_level: float
    battery_mv: int

    mode: str = "text"

class YieldRecord(BaseModel):
    farmer_id: int
    crop: str
    season: str
    year: int
    area_acres: float
    yield_quintals: float
    revenue: float = 0
    expenses: float = 0


# ===== ROUTES =====

@app.get("/")
async def root():
    return {
        "name": "Krishikarm v7 — AI Farming Intelligence",
        "version": "6.0.0",
        "status": "running",
        "features": ["face_recognition", "voice_ai", "llm_advisor", "scheme_matcher", "satellite_data"],
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health():
    ollama = await llm_engine.check_ollama()
    return {
        "status": "healthy",
        "face_engine": face_engine.is_available(),
        "whisper": voice_engine.is_whisper_available(),
        "piper_tts": voice_engine.is_piper_available(),
        "ollama": ollama,
        "database": os.path.exists(farmer_db.DB_PATH),
    }


# --- FACE IDENTIFICATION ---

@app.post("/identify")
async def identify_farmer_route(image: UploadFile = File(...)):
    """Identify a farmer by their face. Returns farmer profile if found, or 'unknown'."""
    image_bytes = await image.read()
    faces = face_engine.detect_faces(image_bytes)

    if not faces:
        return {"status": "no_face", "message": "No face detected. Please look at the camera."}

    face = faces[0]  # Use first (closest) face
    all_farmers = farmer_db.get_all_farmers_with_embeddings()

    if not all_farmers:
        return {
            "status": "no_farmers",
            "message": "No farmers registered yet. Please register first.",
            "face_detected": True,
            "face_info": {"age": face.get('age'), "gender": face.get('gender')}
        }

    farmer_id, confidence, name = face_engine.identify_farmer(face['embedding'], all_farmers)

    if farmer_id:
        farmer = farmer_db.get_farmer(farmer_id)
        token = farmer.get('token')
        return {
            "status": "identified",
            "farmer_id": farmer_id,
            "confidence": round(confidence, 3),
            "farmer": farmer,
            "token": token
        }

    return {
        "status": "unknown",
        "message": "Face not recognized. Would you like to register?",
        "confidence": round(confidence, 3),
        "face_info": {"age": face.get('age'), "gender": face.get('gender')}
    }


@app.post("/register")
async def register_farmer(
    image: UploadFile = File(...),
    data: str = Form(...)
):
    """Register a new farmer with face + profile data."""
    import json
    profile = json.loads(data)
    image_bytes = await image.read()

    # Get face embedding
    faces = face_engine.detect_faces(image_bytes)
    if not faces:
        raise HTTPException(400, "No face detected in image")

    embedding = faces[0]['embedding']

    # Check if already exists
    all_farmers = farmer_db.get_all_farmers_with_embeddings()
    existing_id, score, _ = face_engine.identify_farmer(embedding, all_farmers)
    if existing_id and score > 0.5:
        raise HTTPException(409, f"Farmer already registered (ID: {existing_id}, match: {score:.2f})")

    # Generate secure token
    token = secrets.token_hex(32)
    
    # Create farmer
    farmer_id = farmer_db.create_farmer(
        name=profile['name'],
        village=profile.get('village', ''),
        district=profile.get('district', ''),
        state=profile.get('state', ''),
        language=profile.get('language', 'hi'),
        latitude=profile.get('latitude'),
        longitude=profile.get('longitude'),
        land_acres=profile.get('land_acres', 0),
        crops=profile.get('crops', []),
        face_embedding=embedding,
        phone=profile.get('phone'),
        father_name=profile.get('father_name'),
        irrigation_type=profile.get('irrigation_type'),
        family_members=profile.get('family_members', 4),
        bpl_card=profile.get('bpl_card', 0),
        financial_state=profile.get('financial_state', 'stable'),
        token=token
    )

    farmer = farmer_db.get_farmer(farmer_id)
    logger.info(f"✅ Registered farmer: {profile['name']} (ID: {farmer_id})")

    return {"status": "registered", "farmer_id": farmer_id, "farmer": farmer, "token": token}


# --- CHAT / AI ADVISOR ---

@app.post("/chat")
async def chat_route(request: ChatRequest, current_farmer: dict = Depends(get_current_farmer)):
    """AI-powered chat with farmer context."""
    if request.farmer_id != current_farmer['id']:
        raise HTTPException(403, "Access denied: Farmer ID mismatch")
    
    farmer = current_farmer
    if not farmer:
        raise HTTPException(404, "Farmer not found")

    # Fetch satellite data if farmer has location
    sat_data = None
    weather = None
    if farmer.get('latitude') and farmer.get('longitude'):
        sat_data = await satellite_advisor.get_farm_intelligence(farmer['latitude'], farmer['longitude'])
        weather = {
            "today": f"{sat_data.get('temperature', '--')}°C, {sat_data.get('humidity', '--')}% humidity",
            "forecast_3d": sat_data.get('forecast_3d', '--'),
            "rain_expected": sat_data.get('rain_expected', False),
        } if sat_data else None

    # Match schemes
    schemes = scheme_matcher.match_schemes(farmer)

    # Get conversation history
    history = farmer_db.get_farmer_history(request.farmer_id, limit=6)

    # Query LLM
    response = await llm_engine.chat(
        query=request.query,
        farmer=farmer,
        sat_data=sat_data,
        weather=weather,
        scheme_matches=schemes,
        history=history
    )

    # Log interaction
    farmer_db.log_interaction(
        farmer_id=request.farmer_id,
        query=request.query,
        response=response,
        lang=request.language,
        mode=request.mode,
        sat_data=sat_data
    )

    return {
        "response": response,
        "satellite_data": sat_data,
        "eligible_schemes": schemes[:5],
        "language": request.language
    }


# --- VOICE ---

@app.post("/voice/transcribe")
async def transcribe_route(audio: UploadFile = File(...), language: str = Form("hi")):
    """Transcribe voice audio to text."""
    audio_bytes = await audio.read()
    result = voice_engine.transcribe(audio_bytes, language=language)
    return result


@app.post("/voice/synthesize")
async def synthesize_route(text: str = Form(...), language: str = Form("hi")):
    """Synthesize text to speech audio."""
    audio_bytes = voice_engine.synthesize(text, language=language)
    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/wav")


# --- SCHEMES ---

@app.get("/schemes/{farmer_id}")
async def get_farmer_schemes(farmer_id: int, current_farmer: dict = Depends(get_current_farmer)):
    """Get all eligible schemes for a farmer."""
    if farmer_id != current_farmer['id']:
        raise HTTPException(403, "Access denied: Farmer ID mismatch")
    
    farmer = current_farmer
    if not farmer:
        raise HTTPException(404, "Farmer not found")
    schemes = scheme_matcher.match_schemes(farmer)
    return {"farmer_id": farmer_id, "schemes": schemes, "total": len(schemes)}


# --- FARM DATA ---

@app.get("/farm-data/{farmer_id}")
async def get_farm_data(farmer_id: int, current_farmer: dict = Depends(get_current_farmer)):
    """Get satellite intelligence for a farmer's location."""
    if farmer_id != current_farmer['id']:
        raise HTTPException(403, "Access denied: Farmer ID mismatch")
    
    farmer = current_farmer
    if not farmer:
        raise HTTPException(404, "Farmer not found")
    if not farmer.get('latitude') or not farmer.get('longitude'):
        raise HTTPException(400, "Farmer location not set")

    data = await satellite_advisor.get_farm_intelligence(farmer['latitude'], farmer['longitude'])
    return {"farmer_id": farmer_id, "farm_data": data}


@app.post("/yield")
async def add_yield(record: YieldRecord, current_farmer: dict = Depends(get_current_farmer)):
    """Record yield history for a farmer."""
    if record.farmer_id != current_farmer['id']:
        raise HTTPException(403, "Access denied: Farmer ID mismatch")
    
    farmer = current_farmer
    if not farmer:
        raise HTTPException(404, "Farmer not found")
    farmer_db.add_yield_record(
        record.farmer_id, record.crop, record.season, record.year,
        record.area_acres, record.yield_quintals, record.revenue, record.expenses
    )
    return {"status": "recorded"}


@app.get("/yield/{farmer_id}")
async def get_yield(farmer_id: int, current_farmer: dict = Depends(get_current_farmer)):
    """Get yield history for a farmer."""
    if farmer_id != current_farmer['id']:
        raise HTTPException(403, "Access denied: Farmer ID mismatch")
    history = farmer_db.get_yield_history(farmer_id)
    return {"farmer_id": farmer_id, "yields": history}


@app.get("/farmer/{farmer_id}")
async def get_farmer_route(farmer_id: int, current_farmer: dict = Depends(get_current_farmer)):
    """Get farmer profile."""
    if farmer_id != current_farmer['id']:
        raise HTTPException(403, "Access denied: Farmer ID mismatch")
    return current_farmer


@app.get("/farmers")
async def list_farmers(village: Optional[str] = None, limit: int = 50):
    """List registered farmers."""
    conn = farmer_db.get_db()
    if village:
        rows = conn.execute("SELECT id, name, village, district, state, land_acres, language, created_at FROM farmers WHERE village LIKE ? LIMIT ?", (f"%{village}%", limit)).fetchall()
    else:
        rows = conn.execute("SELECT id, name, village, district, state, land_acres, language, created_at FROM farmers LIMIT ?", (limit,)).fetchall()
    conn.close()
    return {"farmers": [dict(r) for r in rows], "total": len(rows)}


# ===== KISANNET PREDICTION =====

kisan_predictor = None
try:
    import torch
    from train_kisan_net_v2 import KisanNetV2, STATES, IRRIG_TYPES
    from kisan_net import DISTRESS_CLASSES, FINANCIAL_STATES
    import torch.nn.functional as F

    class KisanNetV2Predictor:
        """Production inference wrapper for KisanNet v2."""
        def __init__(self, model_path):
            self.model = KisanNetV2()
            self.device = torch.device('cpu')
            checkpoint = torch.load(model_path, map_location=self.device, weights_only=True)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.metadata = checkpoint.get('metadata', {})
            self.model.eval()
            logger.info(f"🧠 KisanNet v2 loaded: {self.model.count_parameters():,} params")

        @torch.no_grad()
        def predict(self, farmer, sat_data):
            crops = farmer.get('crops', [])
            if isinstance(crops, str):
                crops = [crops]
            irrig = farmer.get('irrigation_type', 'rainfed')
            lat = farmer.get('latitude', 20.0)
            lon = farmer.get('longitude', 80.0)

            feat = torch.tensor([[
                sat_data.get('ndvi', 0.4),
                sat_data.get('soil_moisture', 0.3),
                sat_data.get('temperature', 25) / 50.0,
                sat_data.get('temperature', 25) / 50.0 * 1.1,
                sat_data.get('temperature', 25) / 50.0 * 0.9,
                sat_data.get('humidity', 50) / 100.0,
                min(sat_data.get('rainfall_7d', 0) / 50.0, 1.0),
                sat_data.get('solar', 15) / 30.0,
                2 / 15.0, 1 / 5.0, 10 / 25.0, 0.5, 0.5, 0.9, 0.6, 0.4, 0.0, 0.5,
                0.0, 1.0, 0.0, 1.0,
            ]], dtype=torch.float32)

            ctx = torch.tensor([[
                lat / 35.0, lon / 100.0,
                len(crops) / 5.0,
                1.0 if any(c in crops for c in ['rice', 'wheat']) else 0.0,
                1.0 if any(c in crops for c in ['cotton', 'sugarcane']) else 0.0,
            ]], dtype=torch.float32)

            state = farmer.get('state', 'Other')
            state_idx = torch.tensor([STATES.index(state) if state in STATES else len(STATES)-1])
            irrig_idx = torch.tensor([IRRIG_TYPES.index(irrig) if irrig in IRRIG_TYPES else 0])

            out = self.model(feat, ctx, state_idx, irrig_idx)
            distress = out['distress_score'].item()
            risk_class = out['risk_class'].item()

            return {
                'distress_score': round(distress, 4),
                'distress_label': DISTRESS_CLASSES[min(int(distress * 5), 4)],
                'intervention_days': round(out['intervention_days'].item(), 1),
                'risk_class': DISTRESS_CLASSES[risk_class],
                'risk_probabilities': {
                    DISTRESS_CLASSES[i]: round(p, 4)
                    for i, p in enumerate(F.softmax(out['risk_logits'], dim=-1).squeeze().tolist())
                },
                'model_version': self.metadata.get('version', 'v2'),
                'parameters': self.model.count_parameters(),
                'data_source': 'NASA POWER + Open-Meteo (real)',
            }

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    KISAN_MODEL_PATH = os.getenv("KISAN_MODEL_PATH", os.path.join(BASE_DIR, "models", "kisan_net_v2.pth"))
    kisan_predictor = KisanNetV2Predictor(KISAN_MODEL_PATH)
except Exception as e:
    logger.warning(f"⚠️ KisanNet not loaded: {e}")


@app.get("/predict/{farmer_id}")
async def predict_distress(farmer_id: int, current_farmer: dict = Depends(get_current_farmer)):
    """Run KisanNet v2 crop distress prediction using live satellite data."""
    if not kisan_predictor:
        raise HTTPException(503, "KisanNet model not loaded")

    if farmer_id != current_farmer['id']:
        raise HTTPException(403, "Access denied: Farmer ID mismatch")
    
    farmer = current_farmer

    # Get live satellite data
    lat = farmer.get("latitude", 25.3)
    lon = farmer.get("longitude", 83.0)
    sat_data = await satellite_advisor.get_farm_intelligence(lat, lon)

    # Run KisanNet inference
    prediction = kisan_predictor.predict(
        farmer=farmer,
        sat_data={
            "ndvi": sat_data.get("ndvi", 0.4),
            "soil_moisture": sat_data.get("soil_moisture", 0.3),
            "temperature": sat_data.get("temperature", 25),
            "humidity": sat_data.get("humidity", 50),
            "rainfall_7d": sat_data.get("rainfall_7d", 0),
            "solar": sat_data.get("solar", 15),
        }
    )

    return {
        "farmer_id": farmer_id,
        "farmer_name": farmer.get("name"),
        "location": {"lat": lat, "lon": lon},
        "satellite_data": sat_data,
        "prediction": prediction,
        "timestamp": datetime.now().isoformat(),
    }


# ===== FARMER BUDDY ENDPOINTS =====

import sarvam_engine
import whatsapp_engine
import farming_buddy


class BuddyAskRequest(BaseModel):
    question: str
    farmer_id: Optional[str] = None
    lang: str = "hi"
    lat: Optional[float] = None
    lon: Optional[float] = None


class WhatsAppRequest(BaseModel):
    phone: str
    message: str
    lang: str = "hi"
    farmer_name: str = "Farmer"


@app.post("/buddy/ask")
async def buddy_ask(req: BuddyAskRequest):
    """Ask farming buddy — returns actionable advice in native language."""
    farmer = None
    sat_data = None

    if req.farmer_id:
        farmer = farmer_db.get_farmer(req.farmer_id)
    if req.lat and req.lon:
        try:
            sat_data = await satellite_advisor.get_farm_intelligence(req.lat, req.lon)
        except:
            sat_data = {}

    # Get advice in English
    advice_en = await farming_buddy.get_buddy_advice(req.question, farmer, sat_data, 'en')

    # Translate to native language
    if req.lang != 'en':
        advice_native = await sarvam_engine.translate(advice_en, 'en', req.lang)
    else:
        advice_native = advice_en

    return {
        "advice": advice_native,
        "advice_en": advice_en,
        "lang": req.lang,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/buddy/voice")
async def buddy_voice(audio: UploadFile = File(...), lang: str = Form("hi"),
                      farmer_id: str = Form(None)):
    """Voice note in → advice → voice note out."""
    audio_bytes = await audio.read()

    # STT → text
    transcript = await sarvam_engine.speech_to_text(audio_bytes, lang)
    if not transcript:
        transcript = "help me with farming"

    # Get advice
    farmer = farmer_db.get_farmer(farmer_id) if farmer_id else None
    advice_en = await farming_buddy.get_buddy_advice(transcript, farmer, None, 'en')

    # Translate + TTS
    voice_result = await sarvam_engine.make_voice_reply(advice_en, lang)

    return {
        "transcript": transcript,
        "advice": voice_result.get("text_native", advice_en) if voice_result else advice_en,
        "advice_en": advice_en,
        "audio_base64": voice_result["audio"]["audio_base64"] if voice_result and voice_result.get("audio") else None,
        "lang": lang,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/buddy/tts")
async def buddy_tts(text: str = Form(...), lang: str = Form("hi")):
    """Text-to-speech — generate voice in native language."""
    result = await sarvam_engine.text_to_speech(text, lang)
    if result and result.get("audio_base64"):
        return {"audio_base64": result["audio_base64"], "lang": lang}
    raise HTTPException(400, "TTS generation failed")


@app.post("/buddy/whatsapp")
async def buddy_whatsapp(req: WhatsAppRequest):
    """Send WhatsApp message to farmer."""
    result = await whatsapp_engine.send_whatsapp_advisory(
        req.phone, req.farmer_name, req.message, req.lang
    )
    return result


@app.get("/buddy/marketplace/{crop}")
async def buddy_marketplace(crop: str, state: str = None):
    """Get real-time mandi prices for a crop."""
    prices = await farming_buddy.get_mandi_prices(crop, state)
    return {
        "crop": crop,
        "prices": prices,
        "source": "AgMarkNet / data.gov.in",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/buddy/schemes")
async def buddy_schemes(farmer_id: str = None):
    """Check eligible government schemes."""
    farmer = farmer_db.get_farmer(farmer_id) if farmer_id else {}
    schemes = farming_buddy.check_eligible_schemes(farmer or {})
    return {"schemes": schemes, "count": len(schemes)}


@app.get("/buddy/techniques/{crop}")
async def buddy_techniques(crop: str = "general"):
    """Get budget farming techniques."""
    techniques = farming_buddy.get_budget_techniques(crop)
    return {"crop": crop, "techniques": techniques, "count": len(techniques)}


@app.post("/buddy/translate")
async def buddy_translate(text: str = Form(...), source: str = Form("en"),
                          target: str = Form("hi")):
    """Translate text between Indian languages."""
    translated = await sarvam_engine.translate(text, source, target)
    return {"original": text, "translated": translated, "source": source, "target": target}


# ===== TELEMETRY & AI FUSION =====

@app.post("/api/v1/sync")
async def sync_telemetry(payloads: list[TelemetryPayload]):
    """Sync batched telemetry from Node 2 (via Mobile App)."""
    synced_count = 0
    for p in payloads:
        telemetry_db.insert_telemetry(p.node_id, p.dict())
        synced_count += 1
    return {"status": "success", "synced": synced_count}

@app.get("/api/v1/farm/{farm_id}/analytics")
async def get_farm_analytics(farm_id: str):
    """Retrieve fused analytics based on local node + satellite data."""
    latest = telemetry_db.get_latest_telemetry()
    
    # Sensor data (Local Node 1)
    local_temp = latest[0][5] if latest else 25.0
    local_moisture = latest[0][7] if latest else 40.0
    
    # Simulated Satellite Data (Open-Meteo/NASA POWER)
    satellite_moisture_estimate = 38.0
    satellite_confidence = 0.7
    
    # IoT Hardware Data
    battery_voltage = latest[0][9] if latest and len(latest[0]) > 9 else 3.8 # Vbatt is usually index 9 in TelemetryPacket if we stored it, else assume good battery
    
    # --- Bayesian-Anchored Progressive Scale Graph Network (BAP-GCN) ---
    import fusion_engine
    fused_moisture, fusion_confidence = fusion_engine.fuse_telemetry(
        local_moisture=local_moisture,
        local_temp=local_temp,
        battery_voltage=battery_voltage,
        sat_moisture=satellite_moisture_estimate,
        sat_confidence=satellite_confidence
    )
    
    anomalies = []
    if fused_moisture < 20.0:
        anomalies.append(f"CRITICAL: Soil moisture at {fused_moisture}%. High drought risk.")
    elif abs(local_moisture - satellite_moisture_estimate) > 15.0:
        anomalies.append("WARNING: High variance between local sensor and satellite data. Possible sensor drift/calibration needed.")
        
    return {
        "farm_id": farm_id,
        "fusion_confidence": fusion_confidence,
        "anomalies": anomalies,
        "recommendations": {
            "irrigation": f"Irrigate {int((50.0 - fused_moisture) * 200)} liters today" if fused_moisture < 45.0 else "No irrigation needed.",
            "pest_risk": "High" if (local_temp > 30.0 and fused_moisture > 60.0) else "Low"
        },
        "latest_readings": {
            "raw_local_moisture": local_moisture,
            "satellite_estimate": satellite_moisture_estimate,
            "fused_moisture": fused_moisture,
            "temp": local_temp
        }
    }


# ===== STARTUP =====

@app.on_event("startup")
async def startup():
    logger.info("🛰️ Krishikarm v7 — AI Farming Intelligence starting...")
    farmer_db.init_db()
    logger.info(f"📁 Database: {farmer_db.DB_PATH}")
    logger.info(f"🧠 LLM: {llm_engine.MODEL_NAME} @ {llm_engine.OLLAMA_URL}")
    logger.info(f"👤 Face Engine: {'Available' if face_engine.is_available() else 'Not loaded yet'}")
    kn_status = f"KisanNet: {'v2 loaded' if kisan_predictor else 'not available'}"
    logger.info(f"🧬 {kn_status}")
    logger.info("🤝 Farmer Buddy: Sarvam AI + WhatsApp + Marketplace ready")
    logger.info("✅ Ready to serve farmers!")


# ===== PRODUCTION STATIC FILES =====
# In Docker, FRONTEND_DIR points to the Vite-built dist/ directory.
# This mounts the frontend at / so everything is served on port 8000.
FRONTEND_DIR = os.environ.get("FRONTEND_DIR", "")
if FRONTEND_DIR and Path(FRONTEND_DIR).exists():
    # Serve index.html for SPA fallback
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        file_path = Path(FRONTEND_DIR) / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        # SPA fallback — serve index.html
        index = Path(FRONTEND_DIR) / "index.html"
        if index.exists():
            return FileResponse(index)
        return JSONResponse({"error": "not found"}, status_code=404)
    logger.info(f"🌐 Serving frontend from: {FRONTEND_DIR}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
