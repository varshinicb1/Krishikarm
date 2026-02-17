"""
Farming Buddy — Smart Advisory Engine
══════════════════════════════════════
Personal farming assistant that provides:
  - Marketplace: crop prices, nearest mandis, where to sell/buy
  - Budget techniques: organic, low-cost farming methods
  - Govt schemes: auto-eligibility check + registration guidance
  - Equipment & logistics: rental, transport, storage
"""

import aiohttp
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv

load_dotenv()

# ═══════════════════════════════
# CROP MARKET PRICES (real API)
# ═══════════════════════════════

AGMARKNET_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
MANDI_API_KEY = os.getenv("MANDI_API_KEY")

# Crop Name Mapping (Frontend -> API)
CROP_MAP = {
    "rice": "Paddy(Dhan)(Common)",
    "wheat": "Wheat",
    "cotton": "Cotton",
    "sugarcane": "Sugarcane",
    "soybean": "Soyabean",
    "maize": "Maize",
    "onion": "Onion",
    "potato": "Potato",
    "tomato": "Tomato",
    "groundnut": "Groundnut",
    "mustard": "Mustard",
}

async def get_mandi_prices(crop, state=None, limit=10):
    """Get real-time mandi prices from data.gov.in AgMarkNet (NO MOCK DATA)."""
    
    # Map friendly name to API name
    api_crop = CROP_MAP.get(crop.lower(), crop.capitalize())
    
    params = {
        "api-key": MANDI_API_KEY,
        "format": "json",
        "limit": limit,
        "filters[commodity]": api_crop,
    }
    # Sort by date desc (latest first) if possible, but API doesn't support sort easily.
    # We will sort in code.
    
    if state:
        params["filters[state]"] = state

    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(AGMARKNET_URL, params=params,
                           timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 200:
                    d = await r.json()
                    records = d.get("records", [])
                    
                    # Sort by price desc to show best markets first
                    clean_records = []
                    for rec in records:
                        clean_records.append({
                            "market": rec.get("market", "Unknown Market"),
                            "district": rec.get("district", ""),
                            "state": rec.get("state", ""),
                            "commodity": rec.get("commodity", ""),
                            "variety": rec.get("variety", ""),
                            "min_price": rec.get("min_price", "0"),
                            "max_price": rec.get("max_price", "0"),
                            "modal_price": rec.get("modal_price", "0"),
                            "arrival_date": rec.get("arrival_date", ""),
                        })
                    
                    # Sort: Highest price first (best for farmer)
                    clean_records.sort(key=lambda x: float(x["modal_price"]), reverse=True)
                    return clean_records
                    
                else:
                    err = await r.text()
                    logger.error(f"Mandi API Error {r.status}: {err}")
                    return []
                    
    except Exception as e:
        logger.error(f"Mandi price fetch error: {e}")
        return []

    return []


def _fallback_prices(crop):
    """(DEPRECATED) Mock data - removed per user request."""
    return []


# ═══════════════════════════════
# BUDGET FARMING TECHNIQUES
# ═══════════════════════════════

BUDGET_TECHNIQUES = {
    "general": [
        {"name":"Vermicompost","cost":"₹0-500","desc":"Make free fertilizer from kitchen waste + earthworms. Replaces ₹2000+ of chemical fertilizer.","how":"Layer cow dung, dry leaves, kitchen waste. Add 500g earthworms. Water daily. Ready in 45 days."},
        {"name":"Mulching","cost":"₹0","desc":"Cover soil with dry leaves/straw to retain moisture, reduce watering by 50%.","how":"Spread 3-inch layer of dry grass/leaves around plants. Reduces weeding too."},
        {"name":"Neem spray (pest control)","cost":"₹50-100","desc":"Natural pesticide. Boil neem leaves → spray on crops. Kills 200+ pest types.","how":"Boil 1kg neem leaves in 5L water. Cool, strain, dilute 1:5. Spray early morning."},
        {"name":"Seed treatment (Beejamrit)","cost":"₹20","desc":"Coat seeds with cow dung + urine mix before sowing. Prevents root diseases.","how":"Mix 250g cow dung + 250ml cow urine + 50g lime + 5L water. Soak seeds 20 min."},
        {"name":"Intercropping","cost":"₹0","desc":"Grow 2 crops together (e.g., maize+beans). Increases income 30-40%, reduces pest attacks.","how":"Plant legumes between rows of cereal crops. Beans fix nitrogen for free."},
        {"name":"Jeevamrit (bio fertilizer)","cost":"₹30","desc":"Liquid manure from cow dung. Apply every 15 days. Boosts yield 20%.","how":"Mix 10kg cow dung + 10L cow urine + 2kg jaggery + 2kg pulse flour + 200L water. Ferment 7 days."},
        {"name":"Rainwater harvesting","cost":"₹500-2000","desc":"Collect rainwater in pits/tanks. One good monsoon can fill 3 months of irrigation.","how":"Dig 10×10×3 ft pit near farm. Line with plastic sheet. Channel roof/field runoff into it."},
        {"name":"SRI method (rice)","cost":"₹0","desc":"System of Rice Intensification. Uses 50% less water, 80% less seed, gives 30-50% more yield.","how":"Transplant 8-12 day old single seedlings at 25cm spacing. Keep soil moist, not flooded."},
    ],
    "rice": [
        {"name":"DSR (Direct Seeded Rice)","cost":"₹0","desc":"Skip nursery & transplanting. Saves 4000L water per kg rice. Saves ₹3000/acre labor.","how":"Sow pre-germinated seeds directly in field using seed drill. Maintain moisture, not flooding."},
        {"name":"Azolla biofertilizer","cost":"₹100","desc":"Floating fern that fixes nitrogen. Apply in rice paddies — replaces 30kg urea/acre.","how":"Grow azolla in small pit. Introduce in field after transplanting. Multiplies quickly."},
    ],
    "wheat": [
        {"name":"Zero-till wheat","cost":"₹0","desc":"Sow wheat directly in rice stubble without plowing. Saves ₹2000/acre + 15 days.","how":"Use zero-till drill to sow wheat directly after rice harvest. No burning needed."},
    ],
}

def get_budget_techniques(crop="general"):
    """Get low-cost farming techniques for a crop."""
    techniques = BUDGET_TECHNIQUES.get("general", [])
    if crop.lower() in BUDGET_TECHNIQUES:
        techniques = BUDGET_TECHNIQUES[crop.lower()] + techniques
    return techniques


# ═══════════════════════════════
# GOVERNMENT SCHEMES
# ═══════════════════════════════

GOVT_SCHEMES = [
    {
        "name":"PM-KISAN","full_name":"Pradhan Mantri Kisan Samman Nidhi",
        "benefit":"₹6000/year (₹2000 every 4 months) direct to bank account",
        "eligible":"All farmers with cultivable land (except institutional landholders, income tax payers)",
        "register":"https://pmkisan.gov.in/ → New Farmer Registration → Enter Aadhaar + bank details",
        "docs":"Aadhaar card, bank passbook, land records",
        "auto_eligible": lambda f: f.get("land_acres",0) > 0,
    },
    {
        "name":"PMFBY","full_name":"Pradhan Mantri Fasal Bima Yojana",
        "benefit":"Crop insurance: 1.5% premium for Rabi, 2% for Kharif, 5% for horticulture. Govt pays remaining.",
        "eligible":"All farmers (optional for non-loanee farmers)",
        "register":"Through bank at time of crop loan, or CSC centers, or https://pmfby.gov.in/",
        "docs":"Land records, Aadhaar, bank account, sowing certificate from Patwari",
        "auto_eligible": lambda f: True,
    },
    {
        "name":"KCC","full_name":"Kisan Credit Card",
        "benefit":"Crop loans at 4% interest (after subsidy). Up to ₹3 lakh. Also covers allied activities.",
        "eligible":"All farmers, tenant farmers, sharecroppers",
        "register":"Apply at nearest bank branch (SBI, cooperative bank) with land records + ID proof",
        "docs":"Land records/lease agreement, Aadhaar, 2 passport photos, bank account",
        "auto_eligible": lambda f: True,
    },
    {
        "name":"Soil Health Card","full_name":"Soil Health Card Scheme",
        "benefit":"Free soil testing + nutrient recommendations. Issued every 2 years.",
        "eligible":"All farmers",
        "register":"Visit nearest KVK (Krishi Vigyan Kendra) or https://soilhealth.dac.gov.in/",
        "docs":"Aadhaar, land location details",
        "auto_eligible": lambda f: True,
    },
    {
        "name":"PM-KUSUM","full_name":"Pradhan Mantri Kisan Urja Suraksha",
        "benefit":"Solar pumps with 60% subsidy (30% central + 30% state). Save ₹50000+/year on diesel.",
        "eligible":"Farmers with irrigation need",
        "register":"Through state DISCOM or https://mnre.gov.in/",
        "docs":"Land ownership proof, Aadhaar, bank account, electricity bill (if connected)",
        "auto_eligible": lambda f: f.get("irrigation_type") in ["borewell", "rainfed"],
    },
    {
        "name":"eNAM","full_name":"Electronic National Agriculture Market",
        "benefit":"Sell produce online to mandis across India. Get best price. No middleman commission.",
        "eligible":"Anyone with produce to sell",
        "register":"https://enam.gov.in/ → Farmer Registration → Enter Aadhaar + bank",
        "docs":"Aadhaar, bank passbook, photo",
        "auto_eligible": lambda f: True,
    },
    {
        "name":"PKVY","full_name":"Paramparagat Krishi Vikas Yojana",
        "benefit":"₹50,000/hectare over 3 years for organic farming (cluster of 50+ farmers)",
        "eligible":"Farmers willing to adopt organic farming",
        "register":"Through District Agriculture Officer or KVK",
        "docs":"Land records, group formation (≥50 farmers)",
        "auto_eligible": lambda f: f.get("land_acres",0) > 0,
    },
    {
        "name":"SMAM","full_name":"Sub-Mission on Agricultural Mechanization",
        "benefit":"40-80% subsidy on farm equipment (tractor, harvester, sprayer, thresher)",
        "eligible":"All farmers (higher subsidy for SC/ST, small/marginal farmers)",
        "register":"https://agrimachinery.nic.in/ or District Agriculture Office",
        "docs":"Aadhaar, land records, caste certificate (for SC/ST), quotation from dealer",
        "auto_eligible": lambda f: True,
    },
]


def check_eligible_schemes(farmer):
    """Check which schemes a farmer is eligible for."""
    eligible = []
    for sch in GOVT_SCHEMES:
        try:
            is_eligible = sch["auto_eligible"](farmer)
        except:
            is_eligible = True
        if is_eligible:
            eligible.append({
                "name": sch["name"],
                "full_name": sch["full_name"],
                "benefit": sch["benefit"],
                "how_to_register": sch["register"],
                "documents_needed": sch["docs"],
            })
    return eligible


# ═══════════════════════════════
# BUDDY ADVISOR
# ═══════════════════════════════

async def get_buddy_advice(question, farmer=None, sat_data=None, lang='en'):
    """Generate actionable farming advice based on question + context."""

    # Build context
    ctx_parts = []
    if farmer:
        ctx_parts.append(f"Farmer: {farmer.get('name','')}, {farmer.get('state','')}")
        ctx_parts.append(f"Land: {farmer.get('land_acres','?')} acres, Crops: {farmer.get('crops','?')}")
        ctx_parts.append(f"Irrigation: {farmer.get('irrigation_type','?')}")
    if sat_data:
        ctx_parts.append(f"NDVI: {sat_data.get('ndvi','?')}, Temp: {sat_data.get('temperature','?')}°C")
        ctx_parts.append(f"Soil moisture: {sat_data.get('soil_moisture','?')}, Rain 7d: {sat_data.get('rainfall_7d','?')}mm")

    context = "\n".join(ctx_parts)

    # Simple keyword-based advisor (works offline, no LLM needed)
    q = question.lower()

    if any(w in q for w in ['sell', 'price', 'mandi', 'market', 'bech', 'bazaar']):
        crop = _extract_crop(q)
        prices = await get_mandi_prices(crop)
        if prices:
            advice = f"Current {crop} prices:\n"
            for p in prices[:5]:
                advice += f"  • {p.get('market','?')}: ₹{p.get('modal_price','?')}/quintal\n"
            advice += f"\nTip: Also register on eNAM (enam.gov.in) to access 1000+ mandis online."
        else:
            advice = f"Check local mandi for {crop} prices. Register on eNAM for best rates."

    elif any(w in q for w in ['scheme', 'subsidy', 'sarkari', 'yojana', 'government']):
        schemes = check_eligible_schemes(farmer or {})
        advice = "You are eligible for these schemes:\n"
        for sch in schemes[:5]:
            advice += f"\n• **{sch['name']}**: {sch['benefit']}\n  Register: {sch['how_to_register']}\n"

    elif any(w in q for w in ['budget', 'cheap', 'free', 'sasta', 'organic', 'low cost']):
        crop = _extract_crop(q) or farmer.get('crops',['general'])[0] if farmer else 'general'
        techniques = get_budget_techniques(crop)
        advice = f"Low-cost farming techniques for {crop}:\n"
        for t in techniques[:4]:
            advice += f"\n• **{t['name']}** ({t['cost']}): {t['desc']}\n  How: {t['how']}\n"

    elif any(w in q for w in ['water', 'irrigat', 'paani', 'sichai']):
        sm = sat_data.get('soil_moisture', 0.3) if sat_data else 0.3
        rain = sat_data.get('rain_expected', False) if sat_data else False
        if rain:
            advice = "Rain is expected in the next 3 days. SAVE water — do not irrigate today."
        elif sm < 0.15:
            advice = "Soil is very dry! Irrigate URGENTLY — especially early morning or evening."
        elif sm > 0.35:
            advice = "Soil has good moisture. No irrigation needed today."
        else:
            advice = "Monitor soil — irrigate if no rain by evening. Morning irrigation is most efficient."

    elif any(w in q for w in ['pest', 'disease', 'keeda', 'rog', 'bug']):
        advice = ("Common organic pest remedies:\n"
                  "• Neem spray: Boil 1kg neem leaves in 5L water → spray crops\n"
                  "• Garlic-chilli spray: Blend 100g garlic + 50g chilli + 1L water → spray\n"
                  "• Yellow sticky traps: For whitefly/aphids (₹10 each)\n"
                  "• Trichoderma: Apply to soil to prevent root diseases (₹50/kg)")

    elif any(w in q for w in ['weather', 'mausam', 'rain', 'barish', 'temperature']):
        if sat_data:
            advice = (f"Current conditions:\n"
                     f"• Temperature: {sat_data.get('temperature','?')}°C\n"
                     f"• Humidity: {sat_data.get('humidity','?')}%\n"
                     f"• Rain 7 days: {sat_data.get('rainfall_7d','?')}mm\n"
                     f"• Forecast: {sat_data.get('forecast_3d','?')}\n"
                     f"• Irrigate: {sat_data.get('irrigate_decision','Check with local office')}")
        else:
            advice = "I need your location to give weather. Click on map or tell me your village name."

    else:
        advice = ("I can help with:\n"
                  "• 'Where to sell rice?' — Market prices & mandis\n"
                  "• 'Government schemes' — Eligibility & registration\n"
                  "• 'Budget farming tips' — Low-cost techniques\n"
                  "• 'Water/irrigation' — When to irrigate\n"
                  "• 'Pest problem' — Organic solutions\n"
                  "• 'Weather' — Forecast & advisory\n\n"
                  "Just ask in your language!")

    return advice


def _extract_crop(text):
    """Extract crop name from text."""
    crops = ['rice','wheat','cotton','sugarcane','soybean','maize','groundnut',
             'bajra','jowar','ragi','mustard','onion','potato','tomato','banana',
             'mango','tea','coffee','coconut','turmeric','chilli','pepper',
             'pulses','gram','jute','grapes']
    for c in crops:
        if c in text.lower():
            return c
    return "rice"
