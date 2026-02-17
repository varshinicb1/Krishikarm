"""
Kisan-Eye V6 — LLM Engine
Ollama integration with farm-context prompt engineering.
Provides data-backed advice, not assumptions.
"""

import os
import json
import logging
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.environ.get("LLM_MODEL", "llama3")

# System prompt for the farm advisor
SYSTEM_PROMPT = """You are Krishikarm, an AI farming intelligence assistant deployed across Indian villages.
You MUST:
- Give advice backed by DATA (satellite NDVI, weather, soil moisture, historical yields).
- Never guess — if you don't have data, say "I need more information."
- Be compassionate — many farmers are in financial distress.
- Speak simply — farmers may have limited formal education.
- Give ACTIONABLE steps, not vague advice.
- Know all Indian government schemes (PM-KISAN, PMFBY, KCC, MSP, MGNREGA, etc.)
- Understand Indian crops, seasons (Kharif/Rabi/Zaid), and farming practices.
- If a farmer is in financial distress, ALWAYS mention: Kisan Call Center (1800-180-1551),
  MGNREGA (100-day employment), PM-KISAN (₹6000/year), KCC (4% loans).
- Respond in the farmer's language when possible.

You are NOT a generic chatbot. You are a LIFELINE for farmers. Every answer matters."""


DISTRESS_PROMPT = """CRITICAL: This farmer is in financial distress.
State: {financial_state}
Debt: ₹{debt}
Income: ₹{income}
Land: {land} acres

Provide IMMEDIATE actionable help:
1. Emergency schemes they qualify for
2. Debt restructuring options (KCC interest subvention)
3. Alternative income sources (MGNREGA, dairy, poultry)
4. Mental health support (Kisan Call Center)
5. Free government resources available
BE EMPATHETIC. This person may be in a crisis."""


def _build_context(farmer, sat_data=None, weather=None, scheme_matches=None):
    """Build rich context for the LLM from farmer data + satellite intelligence."""
    ctx = f"""
=== FARMER PROFILE ===
Name: {farmer.get('name', 'Unknown')}
Village: {farmer.get('village', 'Unknown')}, {farmer.get('district', '')}, {farmer.get('state', '')}
Location: {farmer.get('latitude', '--')}°N, {farmer.get('longitude', '--')}°E
Land: {farmer.get('land_acres', 0)} acres
Crops: {', '.join(farmer.get('crops', []))}
Irrigation: {farmer.get('irrigation_type', 'Rain-fed')}
Language: {farmer.get('language', 'hi')}
Financial State: {farmer.get('financial_state', 'stable')}
Annual Income: ₹{farmer.get('annual_income', 0):,.0f}
Debt: ₹{farmer.get('debt_amount', 0):,.0f}
Family Members: {farmer.get('family_members', 4)}
BPL Card: {'Yes' if farmer.get('bpl_card') else 'No'}
"""

    if sat_data:
        ctx += f"""
=== SATELLITE DATA (Real-time) ===
NDVI (Crop Health): {sat_data.get('ndvi', '--')}
Soil Moisture: {sat_data.get('soil_moisture', '--')}
Temperature: {sat_data.get('temperature', '--')}°C
Humidity: {sat_data.get('humidity', '--')}%
Rainfall (7d): {sat_data.get('rainfall_7d', '--')} mm
Solar Radiation: {sat_data.get('solar', '--')} kWh/m²
"""

    if weather:
        ctx += f"""
=== WEATHER FORECAST ===
Today: {weather.get('today', '--')}
Next 3 days: {weather.get('forecast_3d', '--')}
Rain expected: {weather.get('rain_expected', '--')}
"""

    if scheme_matches:
        ctx += "\n=== ELIGIBLE GOVERNMENT SCHEMES ===\n"
        for s in scheme_matches[:10]:
            ctx += f"- {s['name']}: {s['benefit']} (Eligibility: {s['reason']})\n"

    ctx += f"\nCurrent date: {datetime.now().strftime('%Y-%m-%d')}\n"
    ctx += f"Current season: {'Rabi' if datetime.now().month in [10,11,12,1,2,3] else 'Kharif' if datetime.now().month in [6,7,8,9] else 'Zaid'}\n"

    return ctx


async def chat(query, farmer, sat_data=None, weather=None, scheme_matches=None, history=None):
    """
    Send a query to the LLM with full farm context.
    Returns the AI response text.
    """
    context = _build_context(farmer, sat_data, weather, scheme_matches)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add distress prompt if farmer is struggling
    if farmer.get('financial_state') in ('distress', 'critical', 'loss'):
        messages.append({
            "role": "system",
            "content": DISTRESS_PROMPT.format(
                financial_state=farmer.get('financial_state', 'unknown'),
                debt=farmer.get('debt_amount', 0),
                income=farmer.get('annual_income', 0),
                land=farmer.get('land_acres', 0)
            )
        })

    # Add context
    messages.append({"role": "system", "content": f"FARMER CONTEXT:\n{context}"})

    # Add recent conversation history
    if history:
        for h in history[-6:]:
            messages.append({"role": "user", "content": h['query']})
            messages.append({"role": "assistant", "content": h['response']})

    # Add current query
    messages.append({"role": "user", "content": query})

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": MODEL_NAME,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Low temp = more factual
                        "top_p": 0.9,
                        "num_predict": 1024,
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "I apologize, I couldn't process that. Please try again.")

    except httpx.ConnectError:
        logger.error("Cannot connect to Ollama. Is it running?")
        return _fallback_response(query, farmer, scheme_matches)
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return _fallback_response(query, farmer, scheme_matches)


def _fallback_response(query, farmer, scheme_matches=None):
    """Rule-based fallback when LLM is unavailable."""
    lang = farmer.get('language', 'hi')
    q = query.lower()

    if any(w in q for w in ['scheme', 'yojana', 'योजना', 'subsidy', 'सब्सिडी']):
        if scheme_matches:
            lines = [f"• {s['name']}: {s['benefit']}" for s in scheme_matches[:5]]
            return "You may be eligible for:\n" + "\n".join(lines) + "\n\nCall 1800-180-1551 for help applying."
        return "Call Kisan Call Center at 1800-180-1551 (toll-free) for scheme information."

    if any(w in q for w in ['loan', 'कर्ज', 'rin', 'ऋण', 'debt']):
        return ("For farm loans at 4% interest, apply for Kisan Credit Card (KCC) at your nearest bank. "
                "PM-KISAN provides ₹6,000/year direct benefit. "
                "Call NABARD: 1800-425-0012 (toll-free).")

    if any(w in q for w in ['distress', 'loss', 'नुकसान', 'तकलीफ', 'help', 'मदद']):
        return ("I understand you're going through a difficult time. Here's immediate help:\n"
                "1. Kisan Call Center: 1800-180-1551 (24/7, free)\n"
                "2. MGNREGA: 100 days guaranteed employment\n"
                "3. PM-KISAN: ₹6,000/year for all farmers\n"
                "4. PMFBY: File crop insurance claim at 1800-266-0700\n"
                "You are NOT alone. Please reach out.")

    return ("I'm your Krishikarm farming buddy. Ask me about:\n"
            "• Government schemes you qualify for\n"
            "• What to plant this season\n"
            "• Weather forecast for your farm\n"
            "• Loan & subsidy information\n"
            "• Crop health & irrigation advice\n"
            "Call 1800-180-1551 for immediate help.")


async def check_ollama():
    """Check if Ollama is running and the model is available."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            if resp.status_code == 200:
                models = [m['name'] for m in resp.json().get('models', [])]
                return {"available": True, "models": models, "active": MODEL_NAME}
    except Exception:
        pass
    return {"available": False, "models": [], "active": MODEL_NAME}
