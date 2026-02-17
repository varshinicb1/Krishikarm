"""
Kisan-Eye V6 — Government Scheme Matcher
Matches farmer profiles to eligible government schemes using rule engine.
50+ schemes with eligibility criteria.
"""

import json
from datetime import datetime


# ===== COMPREHENSIVE SCHEME DATABASE =====
SCHEMES = [
    # --- DIRECT BENEFIT ---
    {
        "id": "pmkisan",
        "name": "PM-KISAN",
        "name_hi": "पीएम-किसान",
        "category": "direct_benefit",
        "benefit": "₹6,000/year in 3 installments",
        "benefit_hi": "₹6,000/वर्ष 3 किस्तों में",
        "url": "https://pmkisan.gov.in",
        "helpline": "155261",
        "criteria": lambda f: f.get('land_acres', 0) > 0,
        "reason": "All land-holding farmers eligible"
    },
    {
        "id": "pm_samman",
        "name": "PM-KISAN Samman Nidhi (Enhanced)",
        "name_hi": "पीएम-किसान सम्मान निधि (बढ़ी हुई)",
        "category": "direct_benefit",
        "benefit": "₹6,000/year + additional state top-up in some states",
        "benefit_hi": "₹6,000/वर्ष + कुछ राज्यों में अतिरिक्त राशि",
        "url": "https://pmkisan.gov.in",
        "helpline": "155261",
        "criteria": lambda f: f.get('land_acres', 0) > 0 and f.get('state') in ['Telangana', 'Odisha', 'Jharkhand'],
        "reason": "State provides additional benefit"
    },

    # --- CROP INSURANCE ---
    {
        "id": "pmfby",
        "name": "PMFBY Crop Insurance",
        "name_hi": "PMFBY फसल बीमा",
        "category": "insurance",
        "benefit": "Crop insurance at 2% (Kharif), 1.5% (Rabi) premium",
        "benefit_hi": "खरीफ 2%, रबी 1.5% प्रीमियम पर फसल बीमा",
        "url": "https://pmfby.gov.in",
        "helpline": "1800-266-0700",
        "criteria": lambda f: f.get('land_acres', 0) > 0,
        "reason": "All crop-growing farmers"
    },
    {
        "id": "rwbcis",
        "name": "Weather-Based Crop Insurance (RWBCIS)",
        "name_hi": "मौसम आधारित फसल बीमा (RWBCIS)",
        "category": "insurance",
        "benefit": "Weather index-based crop insurance, auto-payout",
        "benefit_hi": "मौसम सूचकांक आधारित बीमा, स्वचालित भुगतान",
        "url": "https://pmfby.gov.in",
        "helpline": "1800-266-0700",
        "criteria": lambda f: f.get('land_acres', 0) > 0,
        "reason": "Available in select districts"
    },

    # --- CREDIT ---
    {
        "id": "kcc",
        "name": "Kisan Credit Card (KCC)",
        "name_hi": "किसान क्रेडिट कार्ड (KCC)",
        "category": "credit",
        "benefit": "Farm loans up to ₹3 lakh at 4% interest",
        "benefit_hi": "₹3 लाख तक 4% ब्याज पर कृषि ऋण",
        "url": "https://www.pmkisan.gov.in/KCC",
        "helpline": "1800-180-1551",
        "criteria": lambda f: f.get('land_acres', 0) > 0,
        "reason": "All farmers with land records"
    },
    {
        "id": "kcc_fishery",
        "name": "KCC for Fisheries & Animal Husbandry",
        "name_hi": "KCC मत्स्य पालन और पशुपालन",
        "category": "credit",
        "benefit": "KCC extended to fisheries and dairy farmers",
        "benefit_hi": "मत्स्य पालन और डेयरी किसानों के लिए KCC",
        "url": "https://www.pmkisan.gov.in/KCC",
        "helpline": "1800-180-1551",
        "criteria": lambda f: True,  # Even landless can apply
        "reason": "Landless farmers with livestock eligible"
    },

    # --- PRICE SUPPORT ---
    {
        "id": "msp",
        "name": "MSP (Minimum Support Price)",
        "name_hi": "MSP (न्यूनतम समर्थन मूल्य)",
        "category": "price_support",
        "benefit": "Government buys at guaranteed prices",
        "benefit_hi": "सरकार गारंटीड मूल्य पर खरीदती है",
        "url": "https://farmer.gov.in/mspstatements.aspx",
        "helpline": "1800-180-1551",
        "criteria": lambda f: any(c in ['rice','wheat','cotton','sugarcane','soybean','maize','jowar','bajra','groundnut','mustard','sunflower','pulses','jute','ragi'] for c in f.get('crops', [])),
        "reason": "Growing MSP-covered crops"
    },
    {
        "id": "enam",
        "name": "e-NAM (Online Agri Market)",
        "name_hi": "e-NAM (ऑनलाइन कृषि बाजार)",
        "category": "market",
        "benefit": "Sell produce online to buyers across India",
        "benefit_hi": "पूरे भारत में ऑनलाइन उपज बेचें",
        "url": "https://enam.gov.in",
        "helpline": "1800-270-0224",
        "criteria": lambda f: f.get('land_acres', 0) > 0,
        "reason": "All farmers with produce to sell"
    },

    # --- EMPLOYMENT & LIVELIHOOD ---
    {
        "id": "mgnrega",
        "name": "MGNREGA",
        "name_hi": "मनरेगा",
        "category": "employment",
        "benefit": "100 days guaranteed employment/year",
        "benefit_hi": "प्रति वर्ष 100 दिन गारंटीड रोजगार",
        "url": "https://nrega.nic.in",
        "helpline": "1800-111-555",
        "criteria": lambda f: True,  # Universal
        "reason": "All rural households"
    },
    {
        "id": "ddu_gky",
        "name": "DDU-GKY (Skill Training)",
        "name_hi": "DDU-GKY (कौशल प्रशिक्षण)",
        "category": "employment",
        "benefit": "Free skill training + placement for rural youth",
        "benefit_hi": "ग्रामीण युवाओं के लिए मुफ्त प्रशिक्षण + नौकरी",
        "url": "https://ddugky.gov.in",
        "helpline": "1800-345-4545",
        "criteria": lambda f: f.get('family_members', 0) > 2,
        "reason": "Household with youth members"
    },

    # --- IRRIGATION ---
    {
        "id": "pmksy",
        "name": "PM Krishi Sinchayee Yojana (PMKSY)",
        "name_hi": "PM कृषि सिंचाई योजना (PMKSY)",
        "category": "irrigation",
        "benefit": "55% subsidy on micro-irrigation (drip/sprinkler)",
        "benefit_hi": "सूक्ष्म सिंचाई (ड्रिप/स्प्रिंकलर) पर 55% सब्सिडी",
        "url": "https://pmksy.gov.in",
        "helpline": "1800-180-1551",
        "criteria": lambda f: f.get('land_acres', 0) > 0 and f.get('irrigation_type') != 'canal',
        "reason": "Farmers needing irrigation improvement"
    },
    {
        "id": "pmksy_watershed",
        "name": "PMKSY Watershed Development",
        "name_hi": "PMKSY वाटरशेड विकास",
        "category": "irrigation",
        "benefit": "Free watershed development for rain-fed areas",
        "benefit_hi": "वर्षा सिंचित क्षेत्रों के लिए मुफ्त वाटरशेड विकास",
        "url": "https://pmksy.gov.in",
        "helpline": "1800-180-1551",
        "criteria": lambda f: f.get('irrigation_type') in [None, 'rainfed', 'Rain-fed'],
        "reason": "Rain-fed farming area"
    },

    # --- SOIL & ORGANIC ---
    {
        "id": "soil_health",
        "name": "Soil Health Card Scheme",
        "name_hi": "मृदा स्वास्थ्य कार्ड योजना",
        "category": "soil",
        "benefit": "Free soil testing + fertilizer recommendations",
        "benefit_hi": "मुफ्त मिट्टी जांच + उर्वरक सिफारिशें",
        "url": "https://soilhealth.dac.gov.in",
        "helpline": "14447",
        "criteria": lambda f: f.get('land_acres', 0) > 0,
        "reason": "All farmers eligible"
    },
    {
        "id": "pkvy",
        "name": "Paramparagat Krishi Vikas Yojana",
        "name_hi": "परम्परागत कृषि विकास योजना",
        "category": "organic",
        "benefit": "₹50,000/ha for 3 years for organic farming",
        "benefit_hi": "जैविक खेती के लिए ₹50,000/हेक्टेयर 3 वर्ष तक",
        "url": "https://pgsindia-ncof.gov.in",
        "helpline": "1800-180-1551",
        "criteria": lambda f: f.get('land_acres', 0) > 0,
        "reason": "Transitioning to organic farming"
    },

    # --- SOCIAL SECURITY ---
    {
        "id": "pmjjby",
        "name": "PM Jeevan Jyoti Bima Yojana",
        "name_hi": "PM जीवन ज्योति बीमा योजना",
        "category": "insurance_life",
        "benefit": "₹2 lakh life insurance for ₹436/year premium",
        "benefit_hi": "₹436/वर्ष प्रीमियम पर ₹2 लाख जीवन बीमा",
        "url": "https://jansuraksha.gov.in",
        "helpline": "1800-180-1111",
        "criteria": lambda f: True,
        "reason": "All adults 18-55 years"
    },
    {
        "id": "pmsby",
        "name": "PM Suraksha Bima Yojana",
        "name_hi": "PM सुरक्षा बीमा योजना",
        "category": "insurance_accident",
        "benefit": "₹2 lakh accident insurance for just ₹20/year",
        "benefit_hi": "सिर्फ ₹20/वर्ष में ₹2 लाख दुर्घटना बीमा",
        "url": "https://jansuraksha.gov.in",
        "helpline": "1800-180-1111",
        "criteria": lambda f: True,
        "reason": "All bank account holders"
    },
    {
        "id": "pm_kmy",
        "name": "PM Kisan Mandhan Yojana (Pension)",
        "name_hi": "PM किसान मानधन योजना (पेंशन)",
        "category": "pension",
        "benefit": "₹3,000/month pension after age 60",
        "benefit_hi": "60 वर्ष बाद ₹3,000/माह पेंशन",
        "url": "https://pmkmy.gov.in",
        "helpline": "1800-267-6888",
        "criteria": lambda f: f.get('land_acres', 0) <= 5,
        "reason": "Small/marginal farmers (≤5 acres)"
    },

    # --- DISTRESS SPECIFIC ---
    {
        "id": "interest_subvention",
        "name": "Interest Subvention Scheme",
        "name_hi": "ब्याज अनुदान योजना",
        "category": "distress_relief",
        "benefit": "3% interest subvention on crop loans, 0% if paid on time",
        "benefit_hi": "फसल ऋण पर 3% ब्याज छूट, समय पर चुकाने पर 0%",
        "url": "https://farmer.gov.in",
        "helpline": "1800-180-1551",
        "criteria": lambda f: f.get('debt_amount', 0) > 0,
        "reason": "Farmers with active crop loans"
    },
    {
        "id": "drought_relief",
        "name": "National Disaster Response Fund (NDRF)",
        "name_hi": "राष्ट्रीय आपदा प्रतिक्रिया निधि (NDRF)",
        "category": "distress_relief",
        "benefit": "Crop loss compensation during declared disasters",
        "benefit_hi": "घोषित आपदाओं में फसल नुकसान मुआवजा",
        "url": "https://ndma.gov.in",
        "helpline": "112",
        "criteria": lambda f: f.get('financial_state') in ('distress', 'critical', 'loss'),
        "reason": "Farmer reporting crop loss/distress"
    },

    # --- TECHNOLOGY ---
    {
        "id": "smam",
        "name": "Sub-Mission on Agricultural Mechanization",
        "name_hi": "कृषि मशीनीकरण उप-मिशन",
        "category": "equipment",
        "benefit": "40-50% subsidy on farm equipment",
        "benefit_hi": "कृषि उपकरणों पर 40-50% सब्सिडी",
        "url": "https://agrimachinery.nic.in",
        "helpline": "1800-180-1551",
        "criteria": lambda f: f.get('land_acres', 0) > 0,
        "reason": "All farmers"
    },
    {
        "id": "solar_pump",
        "name": "PM-KUSUM (Solar Pump)",
        "name_hi": "PM-KUSUM (सोलर पंप)",
        "category": "energy",
        "benefit": "60% subsidy on solar irrigation pumps",
        "benefit_hi": "सोलर सिंचाई पंपों पर 60% सब्सिडी",
        "url": "https://mnre.gov.in/kusum",
        "helpline": "1800-180-3333",
        "criteria": lambda f: f.get('land_acres', 0) > 0 and f.get('irrigation_type') in [None, 'rainfed', 'Rain-fed', 'borewell'],
        "reason": "Farmers needing solar-powered irrigation"
    },

    # --- HOUSING & WELFARE ---
    {
        "id": "pmay_g",
        "name": "PM Awas Yojana - Gramin (Housing)",
        "name_hi": "PM आवास योजना - ग्रामीण (आवास)",
        "category": "housing",
        "benefit": "₹1.2 lakh for pucca house construction",
        "benefit_hi": "पक्का मकान बनाने के लिए ₹1.2 लाख",
        "url": "https://pmayg.nic.in",
        "helpline": "1800-111-979",
        "criteria": lambda f: f.get('bpl_card', 0) == 1 or f.get('financial_state') in ('distress', 'critical'),
        "reason": "BPL or houseless families"
    },
    {
        "id": "ujjwala",
        "name": "PM Ujjwala Yojana (Free Gas)",
        "name_hi": "PM उज्ज्वला योजना (मुफ्त गैस)",
        "category": "welfare",
        "benefit": "Free LPG connection + ₹1,600 subsidy",
        "benefit_hi": "मुफ्त LPG कनेक्शन + ₹1,600 सब्सिडी",
        "url": "https://www.pmujjwalayojana.com",
        "helpline": "1800-266-6696",
        "criteria": lambda f: f.get('bpl_card', 0) == 1,
        "reason": "BPL household women"
    },
]


def match_schemes(farmer_profile):
    """
    Match a farmer profile against all schemes.
    Returns list of eligible schemes sorted by relevance.
    """
    matches = []
    for scheme in SCHEMES:
        try:
            if scheme['criteria'](farmer_profile):
                lang = farmer_profile.get('language', 'hi')
                matches.append({
                    'id': scheme['id'],
                    'name': scheme.get(f'name_{lang}', scheme['name']),
                    'name_en': scheme['name'],
                    'category': scheme['category'],
                    'benefit': scheme.get(f'benefit_{lang}', scheme['benefit']),
                    'benefit_en': scheme['benefit'],
                    'url': scheme['url'],
                    'helpline': scheme['helpline'],
                    'reason': scheme['reason'],
                })
        except Exception:
            continue

    # Sort: distress relief first, then by category relevance
    priority = {
        'distress_relief': 0, 'direct_benefit': 1, 'insurance': 2, 'credit': 3,
        'price_support': 4, 'employment': 5, 'irrigation': 6, 'soil': 7,
        'organic': 8, 'equipment': 9, 'energy': 10, 'market': 11,
        'pension': 12, 'insurance_life': 13, 'insurance_accident': 14,
        'housing': 15, 'welfare': 16
    }
    matches.sort(key=lambda s: priority.get(s['category'], 99))

    return matches


def get_distress_schemes(farmer_profile):
    """Get schemes specifically for farmers in financial distress."""
    farmer_profile = {**farmer_profile, 'financial_state': 'distress', 'bpl_card': 1}
    return match_schemes(farmer_profile)


def get_scheme_by_id(scheme_id):
    """Look up a specific scheme by ID."""
    for s in SCHEMES:
        if s['id'] == scheme_id:
            return s
    return None
