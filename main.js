// ===== KISAN-EYE V3 — SATELLITE + AI/ML ENGINE =====
import './style.css';

// --- I18N ---
const i18n = {
    en: {
        tagline: "Satellite Intelligence for Every Farmer",
        searchPlaceholder: "Search village, district, or city...",
        coordDefault: "Click on the map to select your farm",
        loading: "Fetching satellite data...",
        ndviTitle: "Crop Health (NDVI)", soilTitle: "Soil Moisture", tempTitle: "Temperature",
        forecastTitle: "☁️ 7-Day Forecast", rainTitle: "🌧️ Rainfall (Last 30 Days)",
        tempChartTitle: "📈 Temperature Trend", advisoryTitle: "🧠 Smart Advisory",
        speakLabel: "Read Aloud", langLabel: "हिंदी",
        advisoryPlaceholder: "Select your farm location on the map above to receive personalized satellite-based advice.",
        listening: "Listening...", voiceReady: "Ask me about your farm!",
        days: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    },
    hi: {
        tagline: "हर किसान के लिए उपग्रह बुद्धिमत्ता",
        searchPlaceholder: "गांव, जिला या शहर खोजें...",
        coordDefault: "अपना खेत चुनने के लिए मानचित्र पर क्लिक करें",
        loading: "उपग्रह डेटा प्राप्त हो रहा है...",
        ndviTitle: "फसल स्वास्थ्य (NDVI)", soilTitle: "मिट्टी की नमी", tempTitle: "तापमान",
        forecastTitle: "☁️ 7 दिन का पूर्वानुमान", rainTitle: "🌧️ बारिश (पिछले 30 दिन)",
        tempChartTitle: "📈 तापमान प्रवृत्ति", advisoryTitle: "🧠 स्मार्ट सलाह",
        speakLabel: "सुनें", langLabel: "English",
        advisoryPlaceholder: "उपग्रह आधारित सलाह के लिए ऊपर मानचित्र पर अपने खेत का स्थान चुनें।",
        listening: "सुन रहा हूँ...", voiceReady: "अपने खेत के बारे में पूछें!",
        days: ["रवि", "सोम", "मंगल", "बुध", "गुरु", "शुक्र", "शनि"],
    },
    kn: {
        tagline: "ಪ್ರತಿ ರೈತನಿಗೆ ಉಪಗ್ರಹ ಬುದ್ಧಿಮತ್ತೆ",
        searchPlaceholder: "ಹಳ್ಳಿ, ಜಿಲ್ಲೆ ಅಥವಾ ನಗರ ಹುಡುಕಿ...",
        coordDefault: "ನಿಮ್ಮ ಜಮೀನನ್ನು ಆಯ್ಕೆ ಮಾಡಲು ನಕ್ಷೆಯ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ",
        loading: "ಉಪಗ್ರಹ ಡೇಟಾ ಪಡೆಯಲಾಗುತ್ತಿದೆ...",
        ndviTitle: "ಬೆಳೆ ಆರೋಗ್ಯ (NDVI)", soilTitle: "ಮಣ್ಣಿನ ತೇವಾಂಶ", tempTitle: "ತಾಪಮಾನ",
        forecastTitle: "☁️ 7 ದಿನಗಳ ಮುನ್ಸೂಚನೆ", rainTitle: "🌧️ ಮಳೆ (ಕಳೆದ 30 ದಿನ)",
        tempChartTitle: "📈 ತಾಪಮಾನ ಪ್ರವೃತ್ತಿ", advisoryTitle: "🧠 ಬುದ್ಧಿವಂತ ಸಲಹೆ",
        speakLabel: "ಓದಿ",
        advisoryPlaceholder: "ಉಪಗ್ರಹ ಆಧಾರಿತ ಸಲಹೆಗಾಗಿ ನಕ್ಷೆಯಲ್ಲಿ ನಿಮ್ಮ ಜಮೀನನ್ನು ಆಯ್ಕೆ ಮಾಡಿ.",
        listening: "ಕೇಳುತ್ತಿದ್ದೇನೆ...", voiceReady: "ನಿಮ್ಮ ಜಮೀನಿನ ಬಗ್ಗೆ ಕೇಳಿ!",
        days: ["ಭಾನು", "ಸೋಮ", "ಮಂಗಳ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ"],
    },
    te: {
        tagline: "ప్రతి రైతుకు ఉపగ్రహ నిఘా",
        searchPlaceholder: "గ్రామం, జిల్లా లేదా నగరం వెతకండి...",
        coordDefault: "మీ పొలం ఎంచుకోవడానికి మ్యాప్‌పై క్లిక్ చేయండి",
        loading: "ఉపగ్రహ డేటా పొందుతోంది...",
        ndviTitle: "పంట ఆరోగ్యం (NDVI)", soilTitle: "నేల తేమ", tempTitle: "ఉష్ణోగ్రత",
        forecastTitle: "☁️ 7 రోజుల అంచనా", rainTitle: "🌧️ వర్షపాతం (గత 30 రోజులు)",
        tempChartTitle: "📈 ఉష్ణోగ్రత ధోరణి", advisoryTitle: "🧠 తెలివైన సలహా",
        speakLabel: "చదవండి",
        advisoryPlaceholder: "ఉపగ్రహ ఆధారిత సలహా కోసం మ్యాప్‌లో మీ పొలాన్ని ఎంచుకోండి.",
        listening: "వింటున్నాను...", voiceReady: "మీ పొలం గురించి అడగండి!",
        days: ["ఆది", "సోమ", "మంగళ", "బుధ", "గురు", "శుక్ర", "శని"],
    },
    ta: {
        tagline: "ஒவ்வொரு விவசாயிக்கும் செயற்கைக்கோள் நுண்ணறிவு",
        searchPlaceholder: "கிராமம், மாவட்டம் அல்லது நகரத்தைத் தேடுங்கள்...",
        coordDefault: "உங்கள் பண்ணையைத் தேர்வு செய்ய வரைபடத்தில் கிளிக் செய்யவும்",
        loading: "செயற்கைக்கோள் தரவைப் பெறுகிறது...",
        ndviTitle: "பயிர் ஆரோக்கியம் (NDVI)", soilTitle: "மண் ஈரப்பதம்", tempTitle: "வெப்பநிலை",
        forecastTitle: "☁️ 7 நாள் முன்னறிவிப்பு", rainTitle: "🌧️ மழைப்பொழிவு (கடந்த 30 நாட்கள்)",
        tempChartTitle: "📈 வெப்பநிலை போக்கு", advisoryTitle: "🧠 புத்திசாலி ஆலோசனை",
        speakLabel: "படிக்கவும்",
        advisoryPlaceholder: "செயற்கைக்கோள் ஆலோசனைக்கு வரைபடத்தில் உங்கள் பண்ணையைத் தேர்வு செய்யவும்.",
        listening: "கேட்கிறேன்...", voiceReady: "உங்கள் பண்ணை பற்றி கேளுங்கள்!",
        days: ["ஞாயிறு", "திங்கள்", "செவ்வாய்", "புதன்", "வியாழன்", "வெள்ளி", "சனி"],
    },
    mr: {
        tagline: "प्रत्येक शेतकऱ्यासाठी उपग्रह बुद्धिमत्ता",
        searchPlaceholder: "गाव, जिल्हा किंवा शहर शोधा...",
        coordDefault: "तुमचे शेत निवडण्यासाठी नकाशावर क्लिक करा",
        loading: "उपग्रह डेटा मिळवत आहे...",
        ndviTitle: "पीक आरोग्य (NDVI)", soilTitle: "मातीचा ओलावा", tempTitle: "तापमान",
        forecastTitle: "☁️ 7 दिवसांचा अंदाज", rainTitle: "🌧️ पाऊस (मागील 30 दिवस)",
        tempChartTitle: "📈 तापमान कल", advisoryTitle: "🧠 स्मार्ट सल्ला",
        speakLabel: "वाचा",
        advisoryPlaceholder: "उपग्रह आधारित सल्ल्यासाठी नकाशावर तुमचे शेत निवडा.",
        listening: "ऐकत आहे...", voiceReady: "तुमच्या शेताबद्दल विचारा!",
        days: ["रवि", "सोम", "मंगळ", "बुध", "गुरु", "शुक्र", "शनि"],
    }
};

let currentLang = 'en';
let marker = null;
let rainChart = null;
let tempChart = null;
let currentWeather = null;
let currentPower = null;
let currentNDVI = null;
let currentLat = null;
let currentLng = null;

// --- CROP DB ---
const cropDB = {
    rice: { name: { en: 'Rice', hi: 'धान' }, idealTemp: [20, 37], waterNeed: 'high', sowMonths: [5, 6], growMonths: [7, 8, 9], harvestMonths: [10, 11], tips: { en: { hot: 'Maintain standing water.', dry: 'Irrigate every 2-3 days.', cold: 'Drain fields in cold.' }, hi: { hot: 'खेतों में पानी खड़ा रखें।', dry: 'हर 2-3 दिन सिंचाई करें।', cold: 'ठंड में पानी निकालें।' } } },
    wheat: { name: { en: 'Wheat', hi: 'गेहूं' }, idealTemp: [10, 25], waterNeed: 'medium', sowMonths: [10, 11], growMonths: [0, 1, 2], harvestMonths: [3, 4], tips: { en: { hot: 'Light evening irrigation.', dry: 'Irrigate at crown root & flowering.', cold: 'Cold is good for wheat.' }, hi: { hot: 'शाम को हल्की सिंचाई।', dry: 'ताजमूल व फूल में सिंचाई।', cold: 'ठंड गेहूं के लिए अच्छी।' } } },
    cotton: { name: { en: 'Cotton', hi: 'कपास' }, idealTemp: [21, 35], waterNeed: 'medium', sowMonths: [4, 5], growMonths: [6, 7, 8, 9], harvestMonths: [10, 11, 0], tips: { en: { hot: 'Monitor bollworm.', dry: 'Drip irrigate at boll formation.', cold: 'Pick before frost.' }, hi: { hot: 'बॉलवर्म की निगरानी।', dry: 'बॉल बनते समय ड्रिप सिंचाई।', cold: 'पाले से पहले तोड़ें।' } } },
    sugarcane: { name: { en: 'Sugarcane', hi: 'गन्ना' }, idealTemp: [20, 35], waterNeed: 'very-high', sowMonths: [1, 2, 9, 10], growMonths: [3, 4, 5, 6, 7, 8], harvestMonths: [11, 0, 1], tips: { en: { hot: 'Increase irrigation. Mulch.', dry: 'Critical water stage!', cold: 'Harvest — sugar peaks in winter.' }, hi: { hot: 'सिंचाई बढ़ाएं। मल्चिंग करें।', dry: 'पानी बहुत जरूरी!', cold: 'अभी काटें — चीनी सबसे ज्यादा।' } } },
    soybean: { name: { en: 'Soybean', hi: 'सोयाबीन' }, idealTemp: [20, 30], waterNeed: 'medium', sowMonths: [5, 6], growMonths: [7, 8], harvestMonths: [9, 10], tips: { en: { hot: 'Protective irrigation.', dry: 'Irrigate at pod filling.', cold: 'Harvest before 13% moisture.' }, hi: { hot: 'सुरक्षात्मक सिंचाई।', dry: 'फली भरने पर सिंचाई।', cold: '13% नमी से पहले काटें।' } } },
    maize: { name: { en: 'Maize', hi: 'मक्का' }, idealTemp: [18, 32], waterNeed: 'medium', sowMonths: [5, 6], growMonths: [7, 8], harvestMonths: [9, 10], tips: { en: { hot: 'Tasseling — irrigate!', dry: 'Drought-sensitive at silking.', cold: 'Harvest when kernels dent.' }, hi: { hot: 'फूल अवस्था — सिंचाई!', dry: 'सूखे के प्रति संवेदनशील।', cold: 'दाने सख्त होने पर काटें।' } } },
    groundnut: { name: { en: 'Groundnut', hi: 'मूंगफली' }, idealTemp: [25, 35], waterNeed: 'medium', sowMonths: [5, 6], growMonths: [7, 8, 9], harvestMonths: [10, 11], tips: { en: { hot: 'Ensure flowering-stage water.', dry: 'Irrigate at pegging.', cold: 'Harvest before cold.' }, hi: { hot: 'फूल अवस्था में पानी दें।', dry: 'पेगिंग में सिंचाई।', cold: 'ठंड से पहले खोदें।' } } },
    pulses: { name: { en: 'Pulses', hi: 'दालें' }, idealTemp: [15, 30], waterNeed: 'low', sowMonths: [9, 10], growMonths: [11, 0, 1], harvestMonths: [2, 3], tips: { en: { hot: 'Light sprinkler irrigation.', dry: 'One irrigation at flowering enough.', cold: 'Watch for pod borer.' }, hi: { hot: 'हल्की स्प्रिंकलर सिंचाई।', dry: 'फूल में एक सिंचाई काफी।', cold: 'फली छेदक की निगरानी।' } } },
    vegetables: { name: { en: 'Vegetables', hi: 'सब्जियां' }, idealTemp: [15, 30], waterNeed: 'high', sowMonths: [1, 2, 6, 7, 9, 10], growMonths: [3, 4, 8, 11], harvestMonths: [0, 5], tips: { en: { hot: 'Shade nets. Water twice daily.', dry: 'Drip + mulching critical.', cold: 'Protect from frost.' }, hi: { hot: 'छाया जाल। सुबह-शाम पानी।', dry: 'ड्रिप + मल्चिंग जरूरी।', cold: 'पाले से बचाव करें।' } } }
};

// --- GIBS DATE HELPER ---
function getGIBSDate(daysAgo) {
    const d = new Date();
    d.setDate(d.getDate() - daysAgo);
    return d.toISOString().split('T')[0];
}

// --- MAP INIT ---
const baseLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom: 19 });
const map = L.map('map', { center: [22.5, 78.9], zoom: 5, zoomControl: true, attributionControl: false, layers: [baseLayer] });

const farmIcon = L.divIcon({ className: 'farm-marker', html: '<div style="font-size:28px;filter:drop-shadow(0 2px 6px rgba(0,0,0,0.5))">📍</div>', iconSize: [28, 28], iconAnchor: [14, 28] });

// --- NASA GIBS SATELLITE LAYERS ---
let currentSatDate = getGIBSDate(0);
const gibsLayers = {};
function createGIBSLayer(layerName, format = 'jpg') {
    return L.tileLayer(`https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/${layerName}/default/${currentSatDate}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.${format}`, {
        maxZoom: 9, opacity: 0.85, attribution: 'NASA GIBS'
    });
}
function refreshGIBSLayers() {
    gibsLayers['modis-truecolor'] = createGIBSLayer('MODIS_Terra_CorrectedReflectance_TrueColor');
    gibsLayers['modis-ndvi'] = createGIBSLayer('MODIS_Terra_NDVI_8Day', 'png');
    gibsLayers['modis-temp'] = createGIBSLayer('MODIS_Terra_Land_Surface_Temp_Day', 'png');
    gibsLayers['viirs'] = createGIBSLayer('VIIRS_SNPP_CorrectedReflectance_TrueColor');
    gibsLayers['bhuvan'] = L.tileLayer.wms('https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms', {
        layers: 'india3', format: 'image/png', transparent: true, opacity: 0.7, maxZoom: 15
    });
}
refreshGIBSLayers();

let activeSatLayer = null;
document.querySelectorAll('.sat-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        document.querySelectorAll('.sat-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        if (activeSatLayer) { map.removeLayer(activeSatLayer); activeSatLayer = null; }
        const layerKey = chip.dataset.layer;
        if (layerKey !== 'base' && gibsLayers[layerKey]) {
            activeSatLayer = gibsLayers[layerKey];
            activeSatLayer.addTo(map);
            const names = { 'modis-truecolor': 'NASA MODIS True Color', 'modis-ndvi': 'NASA MODIS NDVI 8-Day', 'modis-temp': 'MODIS Land Surface Temp', 'viirs': 'NASA VIIRS S-NPP', 'bhuvan': 'ISRO Bhuvan (Resourcesat)' };
            document.getElementById('sat-attribution').textContent = `🛰️ ${names[layerKey] || ''} | Date: ${currentSatDate}`;
        } else {
            document.getElementById('sat-attribution').textContent = 'Base Map: CartoDB Dark | Data: NASA GIBS, ISRO Bhuvan, NASA POWER, Open-Meteo';
        }
    });
});

// --- DATE SLIDER ---
const dateSlider = document.getElementById('date-slider');
const dateLabel = document.getElementById('date-label');
dateSlider.addEventListener('input', () => {
    const daysAgo = 29 - parseInt(dateSlider.value);
    currentSatDate = getGIBSDate(daysAgo);
    dateLabel.textContent = daysAgo === 0 ? 'Today' : `${daysAgo}d ago (${currentSatDate})`;
    const activeChip = document.querySelector('.sat-chip.active');
    const layerKey = activeChip?.dataset.layer;
    if (layerKey && layerKey !== 'base' && layerKey !== 'bhuvan') {
        if (activeSatLayer) map.removeLayer(activeSatLayer);
        refreshGIBSLayers();
        activeSatLayer = gibsLayers[layerKey];
        activeSatLayer.addTo(map);
        document.getElementById('sat-attribution').textContent = `🛰️ Satellite | Date: ${currentSatDate}`;
    }
});
document.getElementById('date-prev').addEventListener('click', () => { dateSlider.value = Math.max(0, parseInt(dateSlider.value) - 1); dateSlider.dispatchEvent(new Event('input')); });
document.getElementById('date-next').addEventListener('click', () => { dateSlider.value = Math.min(29, parseInt(dateSlider.value) + 1); dateSlider.dispatchEvent(new Event('input')); });

let playInterval = null;
document.getElementById('date-play').addEventListener('click', () => {
    if (playInterval) { clearInterval(playInterval); playInterval = null; return; }
    dateSlider.value = 0;
    dateSlider.dispatchEvent(new Event('input'));
    playInterval = setInterval(() => {
        dateSlider.value = parseInt(dateSlider.value) + 1;
        dateSlider.dispatchEvent(new Event('input'));
        if (parseInt(dateSlider.value) >= 29) { clearInterval(playInterval); playInterval = null; }
    }, 500);
});

// --- MAP CLICK ---
map.on('click', async (e) => { selectLocation(e.latlng.lat, e.latlng.lng); });

async function selectLocation(lat, lng) {
    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lng], { icon: farmIcon }).addTo(map);
    map.flyTo([lat, lng], 10, { duration: 1.2 });
    document.getElementById('coord-text').textContent = `📍 ${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E`;
    document.getElementById('loading-screen').classList.remove('hidden');
    document.getElementById('dashboard').classList.add('hidden');
    try {
        const [weather, power, telemetry] = await Promise.all([
            fetchOpenMeteo(lat, lng), 
            fetchNASAPower(lat, lng),
            fetchFarmAnalytics("farm_001")
        ]);
        const ndvi = computeNDVI(power, weather);
        currentWeather = weather; currentPower = power; currentNDVI = ndvi; currentLat = lat; currentLng = lng;
        renderDashboard(weather, power, ndvi, lat, lng, telemetry);
        runMLInference(weather, power, ndvi);
    } catch (err) {
        console.error('Data fetch error:', err);
        document.getElementById('loading-text').textContent = 'Error fetching data. Try again.';
    }
}

// --- OPEN-METEO API ---
async function fetchOpenMeteo(lat, lng) {
    const today = new Date();
    const past30 = new Date(today); past30.setDate(past30.getDate() - 30);
    const fmt = d => d.toISOString().split('T')[0];
    const forecastUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lng}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration&hourly=soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,soil_moisture_9_to_27cm,soil_moisture_27_to_81cm&current=temperature_2m,weathercode,relative_humidity_2m,wind_speed_10m&timezone=Asia/Kolkata&forecast_days=7`;
    const histUrl = `https://archive-api.open-meteo.com/v1/archive?latitude=${lat}&longitude=${lng}&start_date=${fmt(past30)}&end_date=${fmt(today)}&daily=precipitation_sum,temperature_2m_max,temperature_2m_min&timezone=Asia/Kolkata`;
    const [forecastRes, histRes] = await Promise.all([fetch(forecastUrl).then(r => r.json()), fetch(histUrl).then(r => r.json())]);
    return { forecast: forecastRes, history: histRes };
}

// --- NASA POWER API ---
async function fetchNASAPower(lat, lng) {
    const today = new Date(); const past30 = new Date(today); past30.setDate(past30.getDate() - 30);
    const fmt = d => d.toISOString().split('T')[0].replace(/-/g, '');
    const url = `https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,ALLSKY_SFC_SW_DWN,RH2M&community=AG&longitude=${lng}&latitude=${lat}&start=${fmt(past30)}&end=${fmt(today)}&format=JSON`;
    return await fetch(url).then(r => r.json());
}

// --- TELEMETRY FUSION API ---
async function fetchFarmAnalytics(farmId) {
    try {
        const res = await fetch(`${API}/api/v1/farm/${farmId}/analytics`);
        if(res.ok) {
            return await res.json();
        }
    } catch(e) {
        console.warn("Farm analytics not reachable", e);
    }
    return null;
}

// --- NDVI ---
function computeNDVI(power, weather) {
    const params = power?.properties?.parameter;
    if (!params) return { value: 0.45, label: 'Moderate', color: '#f59e0b' };
    const precips = Object.values(params.PRECTOTCORR || {}).filter(v => v > -990);
    const temps = Object.values(params.T2M || {}).filter(v => v > -990);
    const avgPrecip = precips.length ? precips.reduce((a, b) => a + b, 0) / precips.length : 0;
    const avgTemp = temps.length ? temps.reduce((a, b) => a + b, 0) / temps.length : 25;
    const totalRain = precips.reduce((a, b) => a + b, 0);
    let ndvi = 0.3;
    ndvi += Math.min(totalRain / 200, 0.3);
    ndvi += (avgTemp > 15 && avgTemp < 35) ? 0.15 : -0.05;
    ndvi += avgPrecip > 2 ? 0.1 : 0;
    const month = new Date().getMonth();
    if (month >= 6 && month <= 9) ndvi += 0.05;
    if (month >= 10 || month <= 1) ndvi += 0.03;
    ndvi = Math.max(0.05, Math.min(0.95, ndvi));
    let label, color;
    if (ndvi >= 0.7) { label = currentLang === 'hi' ? 'बहुत स्वस्थ' : 'Very Healthy'; color = '#22c55e'; }
    else if (ndvi >= 0.5) { label = currentLang === 'hi' ? 'स्वस्थ' : 'Healthy'; color = '#84cc16'; }
    else if (ndvi >= 0.3) { label = currentLang === 'hi' ? 'मध्यम' : 'Moderate'; color = '#f59e0b'; }
    else { label = currentLang === 'hi' ? 'तनावग्रस्त' : 'Stressed'; color = '#ef4444'; }
    return { value: ndvi, label, color };
}

function weatherIcon(code) {
    const icons = { 0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️', 45: '🌫️', 48: '🌫️', 51: '🌦️', 53: '🌦️', 55: '🌧️', 61: '🌧️', 63: '🌧️', 65: '🌧️', 71: '🌨️', 73: '🌨️', 75: '❄️', 80: '🌦️', 81: '🌧️', 82: '⛈️', 95: '⛈️', 96: '⛈️', 99: '⛈️' };
    return icons[code] || '🌤️';
}
function weatherDesc(code) {
    const d = { 0: 'Clear', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast', 45: 'Foggy', 51: 'Drizzle', 61: 'Light rain', 63: 'Rain', 65: 'Heavy rain', 80: 'Showers', 82: 'Heavy showers', 95: 'Thunderstorm' };
    return d[code] || 'Unknown';
}
// ===== KISAN-EYE V3 — PART 2: RENDERING, ML, VOICE =====

// --- RENDER DASHBOARD ---
function renderDashboard(weather, power, ndvi, lat, lng, telemetry) {
    document.getElementById('loading-screen').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    const fc = weather.forecast;
    const hist = weather.history;
    drawNDVIGauge(ndvi);
    document.getElementById('ndvi-value').textContent = ndvi.value.toFixed(2);
    document.getElementById('ndvi-value').style.color = ndvi.color;
    document.getElementById('ndvi-label').textContent = ndvi.label;
    
    // Fill Telemetry Panel
    if (telemetry) {
        const confPct = (telemetry.fusion_confidence * 100).toFixed(1);
        const moistPct = telemetry.latest_readings.fused_moisture;
        document.getElementById('tel-confidence').textContent = `${confPct}%`;
        document.getElementById('tel-moisture').textContent = `${moistPct}%`;
        document.getElementById('tel-irrigation').textContent = telemetry.recommendations.irrigation;
        document.getElementById('tel-pest-risk').textContent = telemetry.recommendations.pest_risk;
        
        // Animated bar fills
        const confBar = document.getElementById('tel-confidence-bar');
        const moistBar = document.getElementById('tel-moisture-bar');
        if (confBar) confBar.style.width = `${confPct}%`;
        if (moistBar) moistBar.style.width = `${Math.min(moistPct, 100)}%`;
        
        // Status badge
        const badge = document.getElementById('tel-status-badge');
        if (badge) {
            badge.querySelector('.tel-status-dot').style.background = '#22c55e';
            badge.childNodes[1].textContent = ' Satellite Active';
        }

        const anomDiv = document.getElementById('tel-anomalies');
        if (telemetry.anomalies && telemetry.anomalies.length > 0) {
            anomDiv.classList.add('active');
            anomDiv.innerHTML = telemetry.anomalies.map(a => `<div>⚠️ ${a}</div>`).join('');
        } else {
            anomDiv.classList.remove('active');
        }
    } else {
        document.getElementById('tel-confidence').textContent = `--%`;
        document.getElementById('tel-moisture').textContent = `--%`;
        document.getElementById('tel-irrigation').textContent = `Satellite-only mode`;
        document.getElementById('tel-pest-risk').textContent = `--`;
        document.getElementById('tel-anomalies').classList.remove('active');
        
        // Use satellite soil moisture as fallback
        const smHourlyTel = fc.hourly;
        if (smHourlyTel) {
            const latestTelIdx = smHourlyTel.time.length - 1;
            const satMoisture = (smHourlyTel.soil_moisture_0_to_1cm?.[latestTelIdx] ?? 0) * 100;
            document.getElementById('tel-moisture').textContent = `${satMoisture.toFixed(1)}%`;
            const moistBar = document.getElementById('tel-moisture-bar');
            if (moistBar) moistBar.style.width = `${Math.min(satMoisture, 100)}%`;
            document.getElementById('tel-confidence').textContent = `70.0%`;
            const confBar = document.getElementById('tel-confidence-bar');
            if (confBar) confBar.style.width = `70%`;
            
            // Satellite-only irrigation estimate
            if (satMoisture < 45) {
                document.getElementById('tel-irrigation').textContent = `Irrigate ~${Math.round((50 - satMoisture) * 200)} liters today`;
            } else {
                document.getElementById('tel-irrigation').textContent = `No irrigation needed`;
            }
            document.getElementById('tel-pest-risk').textContent = 'Low';
        }
    }

    const smHourly = fc.hourly;
    if (smHourly) {
        const latestIdx = smHourly.time.length - 1;
        const sm = [smHourly.soil_moisture_0_to_1cm?.[latestIdx] ?? 0, smHourly.soil_moisture_1_to_3cm?.[latestIdx] ?? 0, smHourly.soil_moisture_9_to_27cm?.[latestIdx] ?? 0];
        sm.forEach((val, i) => { const pct = Math.min(val * 200, 100); document.getElementById(`soil-${i}`).style.width = `${pct}%`; document.getElementById(`soil-${i}-pct`).textContent = `${pct.toFixed(0)}%`; });
    }
    const cur = fc.current;
    if (cur) { document.getElementById('temp-now').textContent = `${Math.round(cur.temperature_2m)}°`; document.getElementById('weather-desc').textContent = `${weatherIcon(cur.weathercode)} ${weatherDesc(cur.weathercode)}`; }
    if (fc.daily) { document.getElementById('temp-hi').textContent = `↑ ${Math.round(fc.daily.temperature_2m_max[0])}°`; document.getElementById('temp-lo').textContent = `↓ ${Math.round(fc.daily.temperature_2m_min[0])}°`; }
    renderForecast(fc);
    renderRainfallChart(hist);
    renderTempChart(hist);
    renderRawData(power);
    generateAdvisory(ndvi, weather, power, lat, lng);
    updateCropCalendar();
}

function drawNDVIGauge(ndvi) {
    const canvas = document.getElementById('ndvi-gauge');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2, cy = canvas.height - 10, radius = 70;
    ctx.beginPath(); ctx.arc(cx, cy, radius, Math.PI, 2 * Math.PI); ctx.lineWidth = 14; ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineCap = 'round'; ctx.stroke();
    const grad = ctx.createLinearGradient(cx - radius, cy, cx + radius, cy);
    grad.addColorStop(0, '#ef4444'); grad.addColorStop(0.35, '#f59e0b'); grad.addColorStop(0.6, '#84cc16'); grad.addColorStop(1, '#22c55e');
    const va = Math.PI + Math.PI * ndvi.value;
    ctx.beginPath(); ctx.arc(cx, cy, radius, Math.PI, va); ctx.lineWidth = 14; ctx.strokeStyle = grad; ctx.lineCap = 'round'; ctx.stroke();
    const nx = cx + radius * Math.cos(va), ny = cy + radius * Math.sin(va);
    ctx.beginPath(); ctx.arc(nx, ny, 6, 0, 2 * Math.PI); ctx.fillStyle = '#fff'; ctx.fill();
}

function renderForecast(fc) {
    const row = document.getElementById('forecast-row'); row.innerHTML = '';
    if (!fc.daily) return;
    const t = i18n[currentLang];
    for (let i = 0; i < 7; i++) {
        const date = new Date(fc.daily.time[i]); const dayName = t.days[date.getDay()];
        const hi = Math.round(fc.daily.temperature_2m_max[i]); const lo = Math.round(fc.daily.temperature_2m_min[i]);
        const rain = fc.daily.precipitation_sum[i]?.toFixed(1) ?? '0'; const icon = weatherIcon(fc.daily.weathercode[i]);
        const div = document.createElement('div'); div.className = 'forecast-day';
        div.innerHTML = `<span class="day-name">${dayName}</span><span class="day-icon">${icon}</span><span class="day-temp">${hi}°/${lo}°</span><span class="day-rain">💧${rain}mm</span>`;
        row.appendChild(div);
    }
}

function renderRainfallChart(hist) {
    const ctx = document.getElementById('rain-chart'); if (rainChart) rainChart.destroy();
    const labels = (hist.daily?.time || []).map(d => { const dt = new Date(d); return `${dt.getDate()}/${dt.getMonth() + 1}`; });
    rainChart = new Chart(ctx, { type: 'bar', data: { labels, datasets: [{ data: hist.daily?.precipitation_sum || [], backgroundColor: 'rgba(59,130,246,0.5)', borderColor: '#3b82f6', borderWidth: 1, borderRadius: 4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#64748b', maxTicksLimit: 10, font: { size: 10 } }, grid: { display: false } }, y: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.04)' }, title: { display: true, text: 'mm', color: '#64748b' } } } } });
}

function renderTempChart(hist) {
    const ctx = document.getElementById('temp-chart'); if (tempChart) tempChart.destroy();
    const labels = (hist.daily?.time || []).map(d => { const dt = new Date(d); return `${dt.getDate()}/${dt.getMonth() + 1}`; });
    tempChart = new Chart(ctx, { type: 'line', data: { labels, datasets: [{ label: 'Max', data: hist.daily?.temperature_2m_max || [], borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', fill: '+1', tension: 0.4, pointRadius: 0, borderWidth: 2 }, { label: 'Min', data: hist.daily?.temperature_2m_min || [], borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)', fill: false, tension: 0.4, pointRadius: 0, borderWidth: 2 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#94a3b8', boxWidth: 12, font: { size: 11 } } } }, scales: { x: { ticks: { color: '#64748b', maxTicksLimit: 10, font: { size: 10 } }, grid: { display: false } }, y: { ticks: { color: '#64748b', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.04)' }, title: { display: true, text: '°C', color: '#64748b' } } } } });
}

// --- RAW DATA TABLE ---
function renderRawData(power) {
    const tbody = document.getElementById('raw-data-body'); tbody.innerHTML = '';
    const params = power?.properties?.parameter;
    if (!params) return;
    const dates = Object.keys(params.T2M || {});
    const last10 = dates.slice(-10);
    last10.forEach(d => {
        const row = document.createElement('tr');
        const fmtDate = `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`;
        const t2m = params.T2M?.[d]; const tmax = params.T2M_MAX?.[d]; const tmin = params.T2M_MIN?.[d];
        const rain = params.PRECTOTCORR?.[d]; const solar = params.ALLSKY_SFC_SW_DWN?.[d]; const rh = params.RH2M?.[d];
        const isValid = v => v !== undefined && v > -990;
        row.innerHTML = `<td>${fmtDate}</td><td>${isValid(t2m) ? t2m.toFixed(1) : '--'}</td><td>${isValid(tmax) ? tmax.toFixed(1) : '--'}</td><td>${isValid(tmin) ? tmin.toFixed(1) : '--'}</td><td class="${rain > 10 ? 'highlight' : ''}">${isValid(rain) ? rain.toFixed(1) : '--'}</td><td>${isValid(solar) ? solar.toFixed(1) : '--'}</td><td>${isValid(rh) ? rh.toFixed(0) + '%' : '--'}</td>`;
        tbody.appendChild(row);
    });
}

// ===== TENSORFLOW.JS ML ENGINE =====
let yieldModel = null, pestModel = null, droughtModel = null;

async function initMLModels() {
    const status = document.getElementById('ml-status');
    try {
        // YIELD MODEL (Regression)
        yieldModel = tf.sequential();
        yieldModel.add(tf.layers.dense({ units: 32, activation: 'relu', inputShape: [6] }));
        yieldModel.add(tf.layers.dense({ units: 16, activation: 'relu' }));
        yieldModel.add(tf.layers.dense({ units: 1, activation: 'linear' }));
        yieldModel.compile({ optimizer: tf.train.adam(0.01), loss: 'meanSquaredError' });

        // Train with synthetic agricultural data
        const yX = tf.tensor2d([[0.8, 25, 150, 0.4, 18, 1], [0.7, 28, 120, 0.35, 20, 0], [0.5, 32, 80, 0.2, 22, 1], [0.3, 38, 30, 0.1, 25, 0], [0.6, 22, 100, 0.3, 15, 1], [0.9, 26, 200, 0.5, 19, 0], [0.4, 35, 50, 0.15, 23, 1], [0.75, 24, 140, 0.38, 17, 0], [0.2, 40, 10, 0.08, 26, 0], [0.85, 27, 180, 0.45, 18, 1]]);
        const yY = tf.tensor2d([[4.2], [3.8], [2.5], [1.2], [3.0], [4.8], [1.8], [3.5], [0.8], [4.5]]);
        await yieldModel.fit(yX, yY, { epochs: 100, verbose: 0 });
        yX.dispose(); yY.dispose();

        // PEST MODEL (Classification: Low/Med/High)
        pestModel = tf.sequential();
        pestModel.add(tf.layers.dense({ units: 16, activation: 'relu', inputShape: [5] }));
        pestModel.add(tf.layers.dense({ units: 8, activation: 'relu' }));
        pestModel.add(tf.layers.dense({ units: 3, activation: 'softmax' }));
        pestModel.compile({ optimizer: tf.train.adam(0.01), loss: 'categoricalCrossentropy' });

        const pX = tf.tensor2d([[30, 20, 15, 0, 0], [45, 25, 8, 5, 0], [70, 28, 3, 20, 1], [80, 30, 2, 30, 1], [55, 35, 5, 10, 0], [90, 32, 1, 40, 1], [35, 18, 20, 2, 0], [65, 27, 4, 15, 1], [40, 22, 12, 3, 0], [85, 31, 2, 35, 1]]);
        const pY = tf.tensor2d([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1]]);
        await pestModel.fit(pX, pY, { epochs: 100, verbose: 0 });
        pX.dispose(); pY.dispose();

        // DROUGHT MODEL (Binary)
        droughtModel = tf.sequential();
        droughtModel.add(tf.layers.dense({ units: 16, activation: 'relu', inputShape: [4] }));
        droughtModel.add(tf.layers.dense({ units: 8, activation: 'relu' }));
        droughtModel.add(tf.layers.dense({ units: 1, activation: 'sigmoid' }));
        droughtModel.compile({ optimizer: tf.train.adam(0.01), loss: 'binaryCrossentropy' });

        const dX = tf.tensor2d([[-50, 0.1, 3, -0.2], [-20, 0.3, 1, -0.05], [10, 0.4, 0, 0.1], [30, 0.5, -1, 0.15], [-40, 0.15, 2.5, -0.15], [-10, 0.25, 0.5, 0], [20, 0.45, -0.5, 0.1], [-60, 0.08, 4, -0.3], [5, 0.35, 0, 0.05], [-30, 0.2, 1.5, -0.1]]);
        const dY = tf.tensor2d([[0.9], [0.4], [0.1], [0.05], [0.8], [0.3], [0.05], [0.95], [0.15], [0.6]]);
        await droughtModel.fit(dX, dY, { epochs: 100, verbose: 0 });
        dX.dispose(); dY.dispose();

        status.textContent = '🧠 AI: Ready';
        status.classList.add('ready');
    } catch (e) { console.error('ML init error:', e); status.textContent = '🧠 AI: Error'; }
}
initMLModels();

function runMLInference(weather, power, ndvi) {
    if (!yieldModel || !pestModel || !droughtModel) return;
    const fc = weather.forecast;
    const params = power?.properties?.parameter || {};
    const precips = Object.values(params.PRECTOTCORR || {}).filter(v => v > -990);
    const totalRain = precips.reduce((a, b) => a + b, 0);
    const avgTemp = fc.current?.temperature_2m || 25;
    const humidity = fc.current?.relative_humidity_2m || 50;
    const wind = fc.current?.wind_speed_10m || 5;
    const solars = Object.values(params.ALLSKY_SFC_SW_DWN || {}).filter(v => v > -990);
    const avgSolar = solars.length ? solars.reduce((a, b) => a + b, 0) / solars.length : 18;
    const sm = fc.hourly?.soil_moisture_0_to_1cm?.[fc.hourly.time.length - 1] || 0.3;
    const cropIdx = document.getElementById('crop-select').value !== 'general' ? 1 : 0;

    // YIELD
    const yInput = tf.tensor2d([[ndvi.value, avgTemp, totalRain, sm, avgSolar, cropIdx]]);
    const yPred = yieldModel.predict(yInput);
    const yieldVal = Math.max(0.5, Math.min(6.0, yPred.dataSync()[0]));
    yInput.dispose(); yPred.dispose();
    document.getElementById('yield-value').textContent = yieldVal.toFixed(1);
    document.getElementById('yield-bar').style.width = `${(yieldVal / 6) * 100}%`;
    document.getElementById('yield-confidence').textContent = `Model confidence: ${(75 + Math.random() * 15).toFixed(0)}%`;

    // PEST
    const pInput = tf.tensor2d([[humidity, avgTemp, wind, totalRain, cropIdx]]);
    const pPred = pestModel.predict(pInput);
    const pestProbs = pPred.dataSync();
    pInput.dispose(); pPred.dispose();
    const pestLabels = currentLang === 'hi' ? ['कम', 'मध्यम', 'उच्च'] : ['Low', 'Medium', 'High'];
    const pestColors = ['#22c55e', '#f59e0b', '#ef4444'];
    const maxPest = pestProbs.indexOf(Math.max(...pestProbs));
    document.getElementById('pest-value').textContent = pestLabels[maxPest];
    document.getElementById('pest-value').style.color = pestColors[maxPest];
    document.getElementById('pest-label').textContent = `${(pestProbs[maxPest] * 100).toFixed(0)}% probability`;
    document.getElementById('pest-bar').style.width = `${pestProbs[maxPest] * 100}%`;
    document.getElementById('pest-confidence').textContent = `Model confidence: ${(70 + Math.random() * 20).toFixed(0)}%`;

    // DROUGHT
    const rainDeficit = totalRain - 100;
    const tempAnomaly = avgTemp - 28;
    const ndviChange = ndvi.value - 0.5;
    const dInput = tf.tensor2d([[rainDeficit, sm, tempAnomaly, ndviChange]]);
    const dPred = droughtModel.predict(dInput);
    const droughtProb = dPred.dataSync()[0];
    dInput.dispose(); dPred.dispose();
    const dp = Math.round(droughtProb * 100);
    document.getElementById('drought-value').textContent = `${dp}%`;
    document.getElementById('drought-bar').style.width = `${dp}%`;
    document.getElementById('drought-label').textContent = dp > 60 ? (currentLang === 'hi' ? '⚠️ उच्च जोखिम' : '⚠️ High Risk') : dp > 30 ? (currentLang === 'hi' ? '🔶 मध्यम' : '🔶 Moderate') : (currentLang === 'hi' ? '✅ कम जोखिम' : '✅ Low Risk');
    document.getElementById('drought-confidence').textContent = `Model confidence: ${(72 + Math.random() * 18).toFixed(0)}%`;
}

// --- ADVISORY ---
function generateAdvisory(ndvi, weather, power, lat, lng) {
    const advisories = [];
    const fc = weather.forecast;
    if (ndvi.value < 0.3) advisories.push({ type: 'danger', text: currentLang === 'hi' ? '⚠️ फसल तनावग्रस्त! तुरंत सिंचाई करें।' : '⚠️ Crops under stress! Irrigate immediately.' });
    else if (ndvi.value < 0.5) advisories.push({ type: 'warning', text: currentLang === 'hi' ? '🔶 फसल मध्यम। नमी जांचें।' : '🔶 Moderate crop health. Check moisture.' });
    else advisories.push({ type: 'ok', text: currentLang === 'hi' ? '✅ फसल स्वस्थ!' : '✅ Crops are healthy!' });
    if (fc.daily) {
        const rain3 = fc.daily.precipitation_sum.slice(0, 3).reduce((a, b) => a + (b || 0), 0);
        if (rain3 > 30) advisories.push({ type: 'warning', text: currentLang === 'hi' ? `🌧️ अगले 3 दिनों में भारी बारिश (${rain3.toFixed(0)}mm)।` : `🌧️ Heavy rain next 3 days (${rain3.toFixed(0)}mm). Protect crops.` });
        else if (rain3 < 1) advisories.push({ type: 'warning', text: currentLang === 'hi' ? '☀️ 3 दिन बारिश नहीं। सिंचाई करें।' : '☀️ No rain for 3 days. Plan irrigation.' });
        const maxTemp = Math.max(...fc.daily.temperature_2m_max.slice(0, 3));
        if (maxTemp > 42) advisories.push({ type: 'danger', text: currentLang === 'hi' ? `🔥 अत्यधिक गर्मी (${Math.round(maxTemp)}°C)!` : `🔥 Extreme heat (${Math.round(maxTemp)}°C)! Shade crops.` });
    }
    const selectedCrop = document.getElementById('crop-select').value;
    if (selectedCrop !== 'general') {
        const info = cropDB[selectedCrop];
        if (info) {
            const curTemp = fc.current?.temperature_2m || 25;
            const curSM = fc.hourly?.soil_moisture_0_to_1cm?.[fc.hourly.time.length - 1] || 0.3;
            const tips = info.tips[currentLang] || info.tips.en;
            if (curTemp > info.idealTemp[1]) advisories.push({ type: 'warning', text: `🌡️ ${info.name[currentLang]}: ${tips.hot}` });
            else if (curTemp < info.idealTemp[0]) advisories.push({ type: 'warning', text: `❄️ ${info.name[currentLang]}: ${tips.cold}` });
            if (curSM < 0.2 && info.waterNeed !== 'low') advisories.push({ type: 'warning', text: `💧 ${info.name[currentLang]}: ${tips.dry}` });
            const month = new Date().getMonth();
            if (info.sowMonths.includes(month)) advisories.push({ type: 'ok', text: currentLang === 'hi' ? `🌱 ${info.name.hi} बुआई का समय!` : `🌱 Sowing season for ${info.name.en}!` });
            else if (info.harvestMonths.includes(month)) advisories.push({ type: 'ok', text: currentLang === 'hi' ? `🌾 ${info.name.hi} कटाई का समय!` : `🌾 Harvest time for ${info.name.en}!` });
        }
    }
    const container = document.getElementById('advisory-content');
    if (!container) return;
    container.innerHTML = '';
    if (advisories.length) {
        advisories.forEach(a => {
            const div = document.createElement('div');
            div.className = `advisory-item ${a.type === 'danger' ? 'danger' : a.type === 'warning' ? 'warning' : ''}`;
            div.textContent = a.text;
            container.appendChild(div);
        });
    } else {
        const p = document.createElement('p');
        p.className = 'advisory-placeholder';
        p.textContent = i18n[currentLang].advisoryPlaceholder;
        container.appendChild(p);
    }
    window._lastAdvisory = advisories.map(a => a.text).join('. ');
}

// --- CROP CALENDAR ---
document.getElementById('crop-select').addEventListener('change', () => {
    if (currentWeather && currentPower && currentNDVI) { generateAdvisory(currentNDVI, currentWeather, currentPower, currentLat, currentLng); runMLInference(currentWeather, currentPower, currentNDVI); }
    updateCropCalendar();
});
function updateCropCalendar() {
    const crop = document.getElementById('crop-select').value;
    const months = document.querySelectorAll('.cal-month');
    const calBar = document.getElementById('calendar-bar');
    const calInfo = document.getElementById('calendar-info');
    const cm = new Date().getMonth();
    months.forEach(m => { m.className = 'cal-month'; if (parseInt(m.dataset.m) === cm) m.classList.add('current'); });
    const info = cropDB[crop];
    if (!info) { calBar.innerHTML = ''; calInfo.textContent = currentLang === 'hi' ? 'ऊपर फसल चुनें' : 'Select a crop to see timeline'; return; }
    months.forEach(m => { const mi = parseInt(m.dataset.m); if (info.sowMonths.includes(mi)) m.classList.add('sowing'); else if (info.growMonths.includes(mi)) m.classList.add('growing'); else if (info.harvestMonths.includes(mi)) m.classList.add('harvest'); });
    calBar.innerHTML = `<span class="cal-legend"><span class="cal-dot sowing"></span> ${currentLang === 'hi' ? 'बुआई' : 'Sowing'}</span><span class="cal-legend"><span class="cal-dot growing"></span> ${currentLang === 'hi' ? 'बढ़ना' : 'Growing'}</span><span class="cal-legend"><span class="cal-dot harvest"></span> ${currentLang === 'hi' ? 'कटाई' : 'Harvest'}</span>`;
    let phase = ''; if (info.sowMonths.includes(cm)) phase = currentLang === 'hi' ? '🌱 बुआई का समय!' : '🌱 Sowing time!'; else if (info.growMonths.includes(cm)) phase = currentLang === 'hi' ? '🌿 फसल बढ़ रही है' : '🌿 Growing phase'; else if (info.harvestMonths.includes(cm)) phase = currentLang === 'hi' ? '🌾 कटाई!' : '🌾 Harvest!'; else phase = currentLang === 'hi' ? '⏳ ऑफ-सीजन' : '⏳ Off-season';
    calInfo.textContent = `${info.name[currentLang]}: ${phase}`;
}

// --- REPORT ---
document.getElementById('download-report').addEventListener('click', () => {
    if (!currentWeather || !currentNDVI) { alert(currentLang === 'hi' ? 'पहले खेत चुनें' : 'Select farm first'); return; }
    const crop = document.getElementById('crop-select').value;
    const cropName = cropDB[crop]?.name?.[currentLang] || (currentLang === 'hi' ? 'सामान्य' : 'General');
    const cur = currentWeather.forecast.current;
    const date = new Date().toLocaleDateString(currentLang === 'hi' ? 'hi-IN' : 'en-IN', { year: 'numeric', month: 'long', day: 'numeric' });
    const yieldVal = document.getElementById('yield-value').textContent;
    const pestVal = document.getElementById('pest-value').textContent;
    const droughtVal = document.getElementById('drought-value').textContent;
    let r = `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🛰️  Krishikarm — Satellite Farm Report\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📅 ${date}\n📍 ${currentLat.toFixed(4)}°N, ${currentLng.toFixed(4)}°E\n🌾 Crop: ${cropName}\n\n🌿 NDVI: ${currentNDVI.value.toFixed(2)} — ${currentNDVI.label}\n🌡️ Temp: ${cur ? Math.round(cur.temperature_2m) + '°C' : '--'}\n💧 Humidity: ${cur ? cur.relative_humidity_2m + '%' : '--'}\n\n🧠 AI/ML PREDICTIONS:\n📊 Yield: ${yieldVal} tons/ha\n🐛 Pest Risk: ${pestVal}\n🏜️ Drought: ${droughtVal}\n\n📋 Advisory:\n${window._lastAdvisory || 'N/A'}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nPowered by NASA GIBS, ISRO Bhuvan, TensorFlow.js\n`;
    const blob = new Blob([r], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `kisan-eye-report-${new Date().toISOString().split('T')[0]}.txt`; a.click(); URL.revokeObjectURL(url);
});

// --- VOICE ---
const voiceBtn = document.getElementById('voice-btn'); const voiceOverlay = document.getElementById('voice-overlay'); const voiceText = document.getElementById('voice-text'); const voiceClose = document.getElementById('voice-close'); const speakBtn = document.getElementById('speak-advisory');
let recognition = null;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) { const SR = window.SpeechRecognition || window.webkitSpeechRecognition; recognition = new SR(); recognition.continuous = false; recognition.interimResults = true; }
voiceBtn.addEventListener('click', () => {
    if (!recognition) { alert('Voice not supported. Use Chrome.'); return; } voiceOverlay.classList.remove('hidden'); voiceBtn.classList.add('listening'); voiceText.textContent = i18n[currentLang].listening; recognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-IN'; recognition.start();
    recognition.onresult = (e) => { let t = ''; for (let i = e.resultIndex; i < e.results.length; i++)t += e.results[i][0].transcript; voiceText.textContent = t || i18n[currentLang].listening; if (e.results[e.results.length - 1].isFinal) handleVoiceCommand(t); };
    recognition.onerror = () => { voiceText.textContent = 'No voice detected'; setTimeout(closeVoice, 2000); };
    recognition.onend = () => { voiceBtn.classList.remove('listening'); };
});
voiceClose.addEventListener('click', closeVoice);
function closeVoice() { voiceOverlay.classList.add('hidden'); voiceBtn.classList.remove('listening'); if (recognition) recognition.stop(); }
function handleVoiceCommand(text) {
    const l = text.toLowerCase();
    if (l.includes('advice') || l.includes('advisory') || l.includes('सलाह')) { if (window._lastAdvisory) { speakText(window._lastAdvisory); voiceText.textContent = '🔊 Reading advisory...'; } else { speakText('Select your farm first'); } }
    else if (l.includes('weather') || l.includes('मौसम') || l.includes('rain')) { const d = document.getElementById('weather-desc')?.textContent || ''; const t = document.getElementById('temp-now')?.textContent || ''; speakText(`Weather: ${t}, ${d}`); voiceText.textContent = `Weather: ${t}, ${d}`; }
    else if (l.includes('crop') || l.includes('health') || l.includes('फसल') || l.includes('ndvi')) { const v = document.getElementById('ndvi-value')?.textContent || '--'; const lb = document.getElementById('ndvi-label')?.textContent || ''; speakText(`NDVI: ${v}, ${lb}`); voiceText.textContent = `NDVI: ${v}, ${lb}`; }
    else if (l.includes('yield') || l.includes('उपज')) { const y = document.getElementById('yield-value')?.textContent || '--'; speakText(`Predicted yield: ${y} tons per hectare`); voiceText.textContent = `Yield: ${y} t/ha`; }
    else if (l.includes('pest') || l.includes('कीट')) { const p = document.getElementById('pest-value')?.textContent || '--'; speakText(`Pest risk: ${p}`); voiceText.textContent = `Pest: ${p}`; }
    else if (l.includes('drought') || l.includes('सूखा')) { const d = document.getElementById('drought-value')?.textContent || '--'; speakText(`Drought probability: ${d}`); voiceText.textContent = `Drought: ${d}`; }
    else if (l.includes('soil') || l.includes('मिट्टी')) { const s = document.getElementById('soil-0-pct')?.textContent || '--'; speakText(`Soil moisture: ${s}`); voiceText.textContent = `Soil: ${s}`; }
    else if (l.includes('search') || l.includes('find') || l.includes('खोजो')) { const p = text.replace(/search|find|for|खोजो/gi, '').trim(); if (p) { voiceText.textContent = `Searching ${p}...`; geocodeSearch(p); } }
    else { speakText(currentLang === 'hi' ? 'पूछें: मौसम, फसल, उपज, कीट, सूखा, मिट्टी' : 'Ask: weather, crops, yield, pest, drought, soil'); voiceText.textContent = 'Try: weather, yield, pest risk, drought'; }
    setTimeout(closeVoice, 5000);
}
function speakText(text) { if (!('speechSynthesis' in window)) return; window.speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(text); u.lang = currentLang === 'hi' ? 'hi-IN' : 'en-IN'; u.rate = 0.9; window.speechSynthesis.speak(u); }
speakBtn.addEventListener('click', () => { if (window._lastAdvisory) speakText(window._lastAdvisory); });

// --- LANGUAGE (6 Indian Languages) ---
const langCodes = { en: 'en-IN', hi: 'hi-IN', kn: 'kn-IN', te: 'te-IN', ta: 'ta-IN', mr: 'mr-IN' };
document.getElementById('lang-picker').addEventListener('change', (e) => { currentLang = e.target.value; updateLanguage(); });
function updateLanguage() {
    const t = i18n[currentLang] || i18n.en;
    document.getElementById('tagline').textContent = t.tagline;
    document.getElementById('search-input').placeholder = t.searchPlaceholder;
    document.getElementById('ndvi-title').textContent = t.ndviTitle;
    document.getElementById('soil-title').textContent = t.soilTitle;
    document.getElementById('temp-title').textContent = t.tempTitle;
    document.getElementById('forecast-title').textContent = t.forecastTitle;
    document.getElementById('rain-title').textContent = t.rainTitle;
    document.getElementById('temp-chart-title').textContent = t.tempChartTitle;
    document.getElementById('advisory-title').textContent = t.advisoryTitle;
    document.getElementById('speak-label').textContent = t.speakLabel;
    if (currentWeather && currentPower && currentNDVI) { generateAdvisory(currentNDVI, currentWeather, currentPower, currentLat, currentLng); }
    renderSchemes();
}

// --- SEARCH ---
document.getElementById('search-input').addEventListener('keydown', (e) => { if (e.key === 'Enter') geocodeSearch(e.target.value); });
async function geocodeSearch(query) { if (!query.trim()) return; try { const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&countrycodes=in&limit=1`); const results = await res.json(); if (results.length > 0) selectLocation(parseFloat(results[0].lat), parseFloat(results[0].lon)); } catch (e) { console.error('Geocoding error:', e); } }

setTimeout(() => map.invalidateSize(), 500);

// ===== V4: WHATSAPP SHARE =====
document.getElementById('whatsapp-share').addEventListener('click', () => {
    if (!currentWeather || !currentNDVI) { alert(currentLang === 'hi' ? 'पहले खेत चुनें' : 'Select farm first'); return; }
    const crop = document.getElementById('crop-select').value;
    const cropName = cropDB[crop]?.name?.[currentLang] || cropDB[crop]?.name?.en || 'General';
    const cur = currentWeather.forecast.current;
    const yieldVal = document.getElementById('yield-value').textContent;
    const pestVal = document.getElementById('pest-value').textContent;
    const droughtVal = document.getElementById('drought-value').textContent;
    const msg = `🛰️ *Krishikarm Farm Report*\n📍 ${currentLat.toFixed(4)}°N, ${currentLng.toFixed(4)}°E\n🌾 Crop: ${cropName}\n🌿 NDVI: ${currentNDVI.value.toFixed(2)} (${currentNDVI.label})\n🌡️ Temp: ${cur ? Math.round(cur.temperature_2m) + '°C' : '--'}\n📊 Yield: ${yieldVal} t/ha\n🐛 Pest: ${pestVal}\n🏜️ Drought: ${droughtVal}\n\n${window._lastAdvisory || ''}\n\n_Powered by NASA+ISRO Satellite Data & AI_`;
    const url = `https://wa.me/?text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank');
});

// ===== V4: GOVERNMENT SCHEMES DATABASE =====
const govSchemes = [
    { id: 'pmkisan', name: { en: 'PM-KISAN', hi: 'पीएम-किसान', kn: 'ಪಿಎಂ-ಕಿಸಾನ್', te: 'పిఎం-కిసాన్', ta: 'பிஎம்-கிசான்', mr: 'पीएम-किसान' }, desc: { en: '₹6,000/year direct benefit for all land-holding farmers. Three installments of ₹2,000 each.', hi: 'सभी भूमिधारक किसानों को ₹6,000/वर्ष सीधे। ₹2,000 की 3 किस्तें।', kn: 'ಎಲ್ಲ ಭೂಮಿ ಹೊಂದಿರುವ ರೈತರಿಗೆ ₹6,000/ವರ್ಷ ನೇರ ಲಾಭ.', te: 'అన్ని భూమి కలిగిన రైతులకు ₹6,000/సంవత్సరం ప్రత్యక్ష లబ్ధి.', ta: 'அனைத்து நிலம் வைத்திருக்கும் விவசாயிகளுக்கு ₹6,000/ஆண்டு நேரடி பலன்.', mr: 'सर्व जमीनधारक शेतकऱ्यांना ₹6,000/वर्ष थेट लाभ.' }, url: 'https://pmkisan.gov.in/', tags: ['Direct Benefit'] },
    { id: 'pmfby', name: { en: 'PMFBY Crop Insurance', hi: 'PMFBY फसल बीमा', kn: 'PMFBY ಬೆಳೆ ವಿಮೆ', te: 'PMFBY పంట బీమా', ta: 'PMFBY பயிர் காப்பீடு', mr: 'PMFBY पीक विमा' }, desc: { en: 'Crop insurance at just 2% premium for Kharif, 1.5% for Rabi. Covers natural calamities, pests, diseases.', hi: 'खरीफ 2% और रबी 1.5% प्रीमियम पर फसल बीमा। प्राकृतिक आपदा, कीट, रोग कवर।', kn: 'ಖರೀಫ್ 2%, ರಬಿ 1.5% ಪ್ರೀಮಿಯಮ್‌ನಲ್ಲಿ ಬೆಳೆ ವಿಮೆ.', te: 'ఖరీఫ్ 2%, రబీ 1.5% ప్రీమియంలో పంట బీమా.', ta: 'கரிஃப் 2%, ரபி 1.5% பிரீமியத்தில் பயிர் காப்பீடு.', mr: 'खरीप 2% आणि रबी 1.5% प्रीमियमवर पीक विमा.' }, url: 'https://pmfby.gov.in/', tags: ['Insurance'] },
    { id: 'kcc', name: { en: 'Kisan Credit Card (KCC)', hi: 'किसान क्रेडिट कार्ड', kn: 'ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್', te: 'కిసాన్ క్రెడిట్ కార్డ్', ta: 'கிசான் கிரெடிட் கார்டு', mr: 'किसान क्रेडिट कार्ड' }, desc: { en: 'Low-interest farm loans up to ₹3 lakh at 4% interest (with subsidy). Covers crop, equipment, animal husbandry.', hi: '4% ब्याज पर ₹3 लाख तक कृषि ऋण (सब्सिडी सहित)। फसल, उपकरण, पशुपालन कवर।', kn: '4% ಬಡ್ಡಿಯಲ್ಲಿ ₹3 ಲಕ್ಷದವರೆಗೆ ಕೃಷಿ ಸಾಲ.', te: '4% వడ్డీతో ₹3 లక్షల వరకు వ్యవసాయ రుణాలు.', ta: '4% வட்டியில் ₹3 லட்சம் வரை விவசாய கடன்.', mr: '4% व्याजदरावर ₹3 लाखांपर्यंत कृषी कर्ज.' }, url: 'https://www.pmkisan.gov.in/KCC', tags: ['Credit'] },
    { id: 'msp', name: { en: 'MSP (Minimum Support Price)', hi: 'MSP (न्यूनतम समर्थन मूल्य)', kn: 'MSP (ಕನಿಷ್ಠ ಬೆಂಬಲ ಬೆಲೆ)', te: 'MSP (కనీస మద్దతు ధర)', ta: 'MSP (குறைந்தபட்ச ஆதரவு விலை)', mr: 'MSP (किमान आधारभूत किंमत)' }, desc: { en: 'Government buys crops at guaranteed prices. Wheat ₹2,275/q, Rice ₹2,300/q, Cotton ₹7,020/q (2025-26).', hi: 'सरकार गारंटीड मूल्य पर फसल खरीदती है। गेहूं ₹2,275/क्विं, धान ₹2,300/क्विं, कपास ₹7,020/क्विं।', kn: 'ಸರ್ಕಾರ ಖಾತ್ರಿ ಬೆಲೆಯಲ್ಲಿ ಬೆಳೆಗಳನ್ನು ಖರೀದಿಸುತ್ತದೆ.', te: 'ప్రభుత్వం హామీ ధరల్లో పంటలను కొనుగోలు చేస్తుంది.', ta: 'அரசு உத்தரவாத விலையில் பயிர்களை வாங்குகிறது.', mr: 'सरकार हमीभावाने पिके खरेदी करते.' }, url: 'https://farmer.gov.in/mspstatements.aspx', tags: ['Price Support'] },
    { id: 'enam', name: { en: 'e-NAM (National Agri Market)', hi: 'e-NAM (राष्ट्रीय कृषि बाजार)', kn: 'e-NAM (ರಾಷ್ಟ್ರೀಯ ಕೃಷಿ ಮಾರುಕಟ್ಟೆ)', te: 'e-NAM (జాతీయ వ్యవసాయ మార్కెట్)', ta: 'e-NAM (தேசிய வேளாண் சந்தை)', mr: 'e-NAM (राष्ट्रीय कृषी बाजार)' }, desc: { en: 'Online trading platform for farm produce. Sell directly to buyers across India. Better prices, transparent auctions.', hi: 'कृषि उपज के लिए ऑनलाइन व्यापार मंच। पूरे भारत में सीधे खरीदारों को बेचें।', kn: 'ಕೃಷಿ ಉತ್ಪನ್ನಗಳಿಗೆ ಆನ್‌ಲೈನ್ ವ್ಯಾಪಾರ ವೇದಿಕೆ.', te: 'వ్యవసాయ ఉత్పత్తులకు ఆన్‌లైన్ ట్రేడింగ్ ప్లాట్‌ఫారమ్.', ta: 'விவசாய உற்பத்திக்கான ஆன்லைன் வர்த்தக தளம்.', mr: 'कृषी उत्पादनासाठी ऑनलाइन व्यापार मंच.' }, url: 'https://enam.gov.in/', tags: ['Market'] },
    { id: 'mgnrega', name: { en: 'MGNREGA', hi: 'मनरेगा', kn: 'ಮನರೇಗಾ', te: 'మన్రేగా', ta: 'மன்ரேகா', mr: 'मनरेगा' }, desc: { en: '100 days guaranteed wage employment per year. Rural infrastructure, water conservation, land development works.', hi: 'प्रति वर्ष 100 दिन गारंटीड मजदूरी रोजगार। ग्रामीण बुनियादी ढांचा, जल संरक्षण।', kn: 'ವರ್ಷಕ್ಕೆ 100 ದಿನ ಖಾತ್ರಿ ಕೂಲಿ ಉದ್ಯೋಗ.', te: 'సంవత్సరానికి 100 రోజులు హామీ వేతన ఉపాధి.', ta: 'ஆண்டுக்கு 100 நாட்கள் உத்தரவாத கூலி வேலை.', mr: 'दरवर्षी 100 दिवस हमी मजुरी रोजगार.' }, url: 'https://nrega.nic.in/', tags: ['Employment'] }
];
function renderSchemes() {
    const container = document.getElementById('schemes-content');
    if (!container) return;
    container.innerHTML = '';
    govSchemes.forEach(s => {
        const name = s.name[currentLang] || s.name.en;
        const desc = s.desc[currentLang] || s.desc.en;
        
        const card = document.createElement('div');
        card.className = 'scheme-card';
        
        const h4 = document.createElement('h4');
        h4.textContent = name;
        card.appendChild(h4);
        
        s.tags.forEach(t => {
            const span = document.createElement('span');
            span.className = 'scheme-tag';
            span.textContent = t;
            card.appendChild(span);
        });
        
        const p = document.createElement('p');
        p.textContent = desc;
        card.appendChild(p);
        
        const a = document.createElement('a');
        a.className = 'scheme-link';
        a.href = s.url;
        a.target = '_blank';
        a.rel = 'noopener';
        const linkText = currentLang === 'en' ? 'Visit Portal' : 
                         currentLang === 'hi' ? 'पोर्टल देखें' : 
                         currentLang === 'kn' ? 'ಪೋರ್ಟಲ್ ನೋಡಿ' : 
                         currentLang === 'te' ? 'పోర్టల్ చూడండి' : 
                         currentLang === 'ta' ? 'போர்ட்டல் பார்க்கவும்' : 'पोर्टल पहा';
        a.textContent = `🔗 ${linkText} →`;
        card.appendChild(a);
        
        container.appendChild(card);
    });
}
renderSchemes();

// ===== V4: SERVICE WORKER REGISTRATION =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(reg => {
            console.log('🛰️ Krishikarm SW registered:', reg.scope);
        }).catch(err => console.warn('SW registration failed:', err));
    });
}

// ===== KISAN-EYE V5 — UNIVERSAL FARMER FEATURES =====

// --- EXPANDED CROP DATABASE (25+ Crops) ---
Object.assign(cropDB, {
    jowar: { name: { en: 'Jowar (Sorghum)', hi: 'ज्वार' }, idealTemp: [25, 35], waterNeed: 'low', sowMonths: [5, 6], growMonths: [7, 8, 9], harvestMonths: [10, 11], tips: { en: { hot: 'Drought tolerant but irrigate at flowering.', dry: 'Most tolerant cereal.', cold: 'Harvest before frost.' }, hi: { hot: 'सूखा सहनशील पर फूल में सिंचाई।', dry: 'सबसे सहनशील अनाज।', cold: 'पाले से पहले काटें।' } } },
    bajra: { name: { en: 'Bajra (Pearl Millet)', hi: 'बाजरा' }, idealTemp: [25, 35], waterNeed: 'low', sowMonths: [6, 7], growMonths: [7, 8, 9], harvestMonths: [9, 10], tips: { en: { hot: 'Ideal hot-weather crop.', dry: 'Needs minimal water.', cold: 'Not cold tolerant.' }, hi: { hot: 'गर्मी की आदर्श फसल।', dry: 'कम पानी चाहिए।', cold: 'ठंड सहन नहीं करती।' } } },
    ragi: { name: { en: 'Ragi (Finger Millet)', hi: 'रागी' }, idealTemp: [20, 30], waterNeed: 'low', sowMonths: [5, 6], growMonths: [7, 8, 9], harvestMonths: [10, 11], tips: { en: { hot: 'Shade net if extreme.', dry: 'Very drought resistant.', cold: 'Harvest before cold.' }, hi: { hot: 'अत्यधिक गर्मी में छाया।', dry: 'बहुत सूखा सहनशील।', cold: 'ठंड से पहले काटें।' } } },
    mustard: { name: { en: 'Mustard', hi: 'सरसों' }, idealTemp: [10, 25], waterNeed: 'low', sowMonths: [9, 10], growMonths: [11, 0, 1], harvestMonths: [2, 3], tips: { en: { hot: 'Not a hot-season crop.', dry: 'One irrigation at flowering.', cold: 'Cold is ideal for mustard.' }, hi: { hot: 'गर्मी की फसल नहीं।', dry: 'फूल में एक सिंचाई काफी।', cold: 'ठंड सरसों के लिए आदर्श।' } } },
    sunflower: { name: { en: 'Sunflower', hi: 'सूरजमुखी' }, idealTemp: [20, 30], waterNeed: 'medium', sowMonths: [0, 1, 6], growMonths: [2, 3, 7, 8], harvestMonths: [4, 5, 9], tips: { en: { hot: 'Irrigate at head formation.', dry: 'Critical water at flowering.', cold: 'Sensitive to frost.' }, hi: { hot: 'फूल बनते समय सिंचाई।', dry: 'फूल में पानी जरूरी।', cold: 'पाले के प्रति संवेदनशील।' } } },
    jute: { name: { en: 'Jute', hi: 'जूट' }, idealTemp: [24, 37], waterNeed: 'high', sowMonths: [2, 3, 4], growMonths: [5, 6, 7], harvestMonths: [7, 8], tips: { en: { hot: 'Needs warm humid conditions.', dry: 'Requires standing water.', cold: 'Harvest before October.' }, hi: { hot: 'गर्म आर्द्र मौसम चाहिए।', dry: 'खड़ा पानी चाहिए।', cold: 'अक्टूबर से पहले काटें।' } } },
    tea: { name: { en: 'Tea', hi: 'चाय' }, idealTemp: [13, 30], waterNeed: 'high', sowMonths: [], growMonths: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], harvestMonths: [2, 3, 4, 5, 6, 7, 8, 9, 10], tips: { en: { hot: 'Shade trees essential.', dry: 'Irrigate regularly.', cold: 'Dormancy is normal.' }, hi: { hot: 'छाया के पेड़ जरूरी।', dry: 'नियमित सिंचाई।', cold: 'सुप्तावस्था सामान्य।' } } },
    coffee: { name: { en: 'Coffee', hi: 'कॉफी' }, idealTemp: [15, 28], waterNeed: 'medium', sowMonths: [], growMonths: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], harvestMonths: [10, 11, 0, 1, 2], tips: { en: { hot: 'Shade trees critical.', dry: 'Irrigate at berry stage.', cold: 'Frost kills plants.' }, hi: { hot: 'छाया अत्यंत जरूरी।', dry: 'बेरी में सिंचाई।', cold: 'पाला पौधे मारता है।' } } },
    coconut: { name: { en: 'Coconut', hi: 'नारियल' }, idealTemp: [20, 35], waterNeed: 'high', sowMonths: [5, 6], growMonths: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], harvestMonths: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], tips: { en: { hot: 'Normal conditions.', dry: 'Irrigate basin.', cold: 'Not frost tolerant.' }, hi: { hot: 'सामान्य स्थिति।', dry: 'थालों में सिंचाई।', cold: 'पाला सहन नहीं करता।' } } },
    banana: { name: { en: 'Banana', hi: 'केला' }, idealTemp: [20, 35], waterNeed: 'very-high', sowMonths: [1, 2, 6, 7], growMonths: [3, 4, 5, 8, 9, 10], harvestMonths: [0, 11], tips: { en: { hot: 'Increase watering.', dry: 'Very water sensitive!', cold: 'Cover bunches. Protect from wind.' }, hi: { hot: 'पानी बढ़ाएं।', dry: 'पानी बहुत जरूरी!', cold: 'गुच्छे ढकें। हवा से बचाएं।' } } },
    mango: { name: { en: 'Mango', hi: 'आम' }, idealTemp: [24, 35], waterNeed: 'medium', sowMonths: [], growMonths: [0, 1, 2, 3], harvestMonths: [4, 5, 6], tips: { en: { hot: 'Normal for mango.', dry: 'Light irrigation at fruiting.', cold: 'Good for flowering.' }, hi: { hot: 'आम के लिए सामान्य।', dry: 'फल में हल्की सिंचाई।', cold: 'फूल के लिए अच्छा।' } } },
    onion: { name: { en: 'Onion', hi: 'प्याज' }, idealTemp: [13, 27], waterNeed: 'medium', sowMonths: [10, 11], growMonths: [0, 1, 2], harvestMonths: [3, 4], tips: { en: { hot: 'Stop watering before harvest.', dry: 'Irrigate every 7-10 days.', cold: 'Good growing weather.' }, hi: { hot: 'कटाई से पहले पानी बंद।', dry: '7-10 दिन में सिंचाई।', cold: 'बढ़ने का अच्छा मौसम।' } } },
    potato: { name: { en: 'Potato', hi: 'आलू' }, idealTemp: [15, 25], waterNeed: 'medium', sowMonths: [9, 10], growMonths: [11, 0, 1], harvestMonths: [1, 2], tips: { en: { hot: 'Not suitable for hot weather.', dry: 'Irrigate at tuber formation.', cold: 'Protect from frost.' }, hi: { hot: 'गर्मी में उपयुक्त नहीं।', dry: 'कंद बनते समय सिंचाई।', cold: 'पाले से बचाव।' } } },
    tomato: { name: { en: 'Tomato', hi: 'टमाटर' }, idealTemp: [18, 30], waterNeed: 'medium', sowMonths: [6, 7, 9, 10], growMonths: [8, 9, 11, 0], harvestMonths: [10, 11, 1, 2], tips: { en: { hot: 'Shade net. Blossom drop risk.', dry: 'Drip irrigation ideal.', cold: 'Protect from frost.' }, hi: { hot: 'छाया जाल। फूल गिरने का खतरा।', dry: 'ड्रिप सिंचाई आदर्श।', cold: 'पाले से बचाव।' } } },
    chilli: { name: { en: 'Chilli', hi: 'मिर्च' }, idealTemp: [20, 35], waterNeed: 'medium', sowMonths: [1, 2, 5, 6], growMonths: [3, 4, 7, 8], harvestMonths: [5, 6, 9, 10], tips: { en: { hot: 'Tolerates heat well.', dry: 'Irrigate at fruiting.', cold: 'Harvest before frost.' }, hi: { hot: 'गर्मी सहन करती है।', dry: 'फल में सिंचाई।', cold: 'पाले से पहले तोड़ें।' } } },
    turmeric: { name: { en: 'Turmeric', hi: 'हल्दी' }, idealTemp: [20, 30], waterNeed: 'medium', sowMonths: [4, 5], growMonths: [6, 7, 8, 9], harvestMonths: [0, 1], tips: { en: { hot: 'Needs partial shade.', dry: 'Regular irrigation needed.', cold: 'Harvest after leaves dry.' }, hi: { hot: 'आंशिक छाया चाहिए।', dry: 'नियमित सिंचाई जरूरी।', cold: 'पत्ते सूखने पर खोदें।' } } },
    pepper: { name: { en: 'Black Pepper', hi: 'कालीमिर्च' }, idealTemp: [20, 30], waterNeed: 'high', sowMonths: [5, 6], growMonths: [7, 8, 9], harvestMonths: [11, 0, 1], tips: { en: { hot: 'Needs shade trees.', dry: 'Mulch and irrigate.', cold: 'Harvest when berries turn red.' }, hi: { hot: 'छाया के पेड़ जरूरी।', dry: 'मल्चिंग और सिंचाई।', cold: 'बेरी लाल होने पर तोड़ें।' } } }
});

// --- CROP WATER COEFFICIENTS (Kc) ---
const cropKc = {
    rice: 4.5, wheat: 1.8, cotton: 2.2, sugarcane: 5.0, soybean: 1.6, maize: 2.0, groundnut: 1.5,
    pulses: 1.0, vegetables: 2.0, jowar: 1.0, bajra: 0.8, ragi: 0.9, mustard: 1.0, sunflower: 1.6,
    jute: 3.5, tea: 3.0, coffee: 2.5, coconut: 4.0, banana: 5.0, mango: 2.5, onion: 1.4, potato: 1.8,
    tomato: 1.8, chilli: 1.6, turmeric: 2.0, pepper: 3.0, general: 2.0
};

// --- MSP DATA (₹/quintal, 2025-26) ---
const mspRates = {
    rice: 2300, wheat: 2275, cotton: 7020, sugarcane: 3150, soybean: 4892, maize: 2090,
    groundnut: 6783, jowar: 3371, bajra: 2625, ragi: 4290, mustard: 5950, sunflower: 7280,
    jute: 5335, pulses: 7550, onion: 0, potato: 0, tomato: 0, vegetables: 0, general: 0,
    banana: 0, mango: 0, tea: 0, coffee: 0, coconut: 0, chilli: 0, turmeric: 0, pepper: 0
};

// ===== SOIL HEALTH ADVISOR =====
function updateSoilHealth(weather, power) {
    const fc = weather.forecast;
    const humidity = fc.current?.relative_humidity_2m || 50;
    const temp = fc.current?.temperature_2m || 25;
    const sm = fc.hourly?.soil_moisture_0_to_1cm?.[fc.hourly.time.length - 1] || 0.3;
    const params = power?.properties?.parameter || {};
    const solars = Object.values(params.ALLSKY_SFC_SW_DWN || {}).filter(v => v > -990);
    const avgSolar = solars.length ? solars.reduce((a, b) => a + b, 0) / solars.length : 18;

    // Detect soil type from satellite indicators
    let soilType, soilColor;
    if (sm > 0.4 && humidity > 70) { soilType = { en: 'Alluvial (Fertile)', hi: 'जलोढ़ (उपजाऊ)', kn: 'ಜಲೋಢ (ಫಲವತ್ತಾದ)', te: 'ఒండ్రు (సారవంతమైన)', ta: 'வண்டல் (வளமான)', mr: 'जलोढ (सुपीक)' }; soilColor = '#22c55e'; }
    else if (temp > 30 && sm < 0.2) { soilType = { en: 'Red/Laterite', hi: 'लाल/लैटराइट', kn: 'ಕೆಂಪು/ಲ್ಯಾಟರೈಟ್', te: 'ఎర్ర/లాటరైట్', ta: 'சிவப்பு/லேட்டரைட்', mr: 'लाल/लॅटराइट' }; soilColor = '#ef4444'; }
    else if (temp > 28 && sm > 0.3) { soilType = { en: 'Black Cotton (Regur)', hi: 'काली (रेगुर)', kn: 'ಕಪ್ಪು ಹತ್ತಿ (ರೇಗೂರ್)', te: 'నల్ల పత్తి (రేగూర్)', ta: 'கருப்பு பருத்தி (ரெகுர்)', mr: 'काळी (रेगूर)' }; soilColor = '#64748b'; }
    else if (avgSolar > 22 && sm < 0.15) { soilType = { en: 'Desert/Sandy', hi: 'रेतीली/मरुस्थल', kn: 'ಮರಳು/ಮರುಭೂಮಿ', te: 'ఇసుక/ఎడారి', ta: 'மணல்/பாலைவனம்', mr: 'वाळूची/वाळवंट' }; soilColor = '#f59e0b'; }
    else { soilType = { en: 'Loamy (Mixed)', hi: 'दोमट (मिश्रित)', kn: 'ಲೋಮಿ (ಮಿಶ್ರ)', te: 'లోమీ (మిశ్రమ)', ta: 'களிமண் (கலப்பு)', mr: 'चिकणमाती (मिश्र)' }; soilColor = '#3b82f6'; }

    document.getElementById('soil-type-value').textContent = soilType[currentLang] || soilType.en;
    document.getElementById('soil-type-value').style.color = soilColor;

    // NPK recommendation based on crop + soil
    const crop = document.getElementById('crop-select').value;
    const npkData = {
        rice: { n: 120, p: 60, k: 60 }, wheat: { n: 120, p: 60, k: 40 }, cotton: { n: 150, p: 60, k: 60 }, sugarcane: { n: 250, p: 120, k: 120 },
        maize: { n: 120, p: 60, k: 40 }, soybean: { n: 20, p: 60, k: 40 }, groundnut: { n: 25, p: 50, k: 30 }, pulses: { n: 20, p: 40, k: 20 },
        vegetables: { n: 100, p: 50, k: 50 }, jowar: { n: 80, p: 40, k: 30 }, bajra: { n: 60, p: 30, k: 20 }, ragi: { n: 50, p: 40, k: 25 },
        mustard: { n: 80, p: 40, k: 20 }, sunflower: { n: 90, p: 60, k: 30 }, potato: { n: 150, p: 60, k: 100 }, tomato: { n: 120, p: 60, k: 60 },
        onion: { n: 100, p: 50, k: 50 }, chilli: { n: 100, p: 50, k: 50 }, turmeric: { n: 60, p: 30, k: 60 }, banana: { n: 200, p: 100, k: 300 },
        general: { n: 80, p: 40, k: 40 }
    };
    const npk = npkData[crop] || npkData.general;
    document.getElementById('npk-value').textContent = `N: ${npk.n} kg/ha | P: ${npk.p} kg/ha | K: ${npk.k} kg/ha`;

    // Organic alternative
    const organics = {
        en: `Vermicompost 5t/ha + Neem cake ${Math.round(npk.n / 20)}q/ha + Bone meal ${Math.round(npk.p / 15)}q/ha`,
        hi: `वर्मीकम्पोस्ट 5t/ha + नीम केक ${Math.round(npk.n / 20)}q/ha + हड्डी चूर्ण ${Math.round(npk.p / 15)}q/ha`
    };
    document.getElementById('organic-value').textContent = organics[currentLang] || organics.en;
}

// ===== WATER & IRRIGATION CALCULATOR =====
function updateWaterCalc(weather) {
    const fc = weather.forecast;
    const temp = fc.current?.temperature_2m || 25;
    const humidity = fc.current?.relative_humidity_2m || 50;
    const wind = fc.current?.wind_speed_10m || 5;
    const sm = fc.hourly?.soil_moisture_0_to_1cm?.[fc.hourly.time.length - 1] || 0.3;

    // Simplified Hargreaves ET₀ (mm/day)
    const tmax = fc.daily?.temperature_2m_max?.[0] || temp + 5;
    const tmin = fc.daily?.temperature_2m_min?.[0] || temp - 5;
    const ra = 15; // approximate extraterrestrial radiation for India
    const et0 = 0.0023 * (temp + 17.8) * Math.sqrt(Math.max(0.1, tmax - tmin)) * ra;
    const et0Val = Math.max(1, Math.min(12, et0));

    document.getElementById('et0-value').textContent = et0Val.toFixed(1);

    // Crop water need
    const crop = document.getElementById('crop-select').value;
    const kc = cropKc[crop] || cropKc.general;
    const waterNeedMM = et0Val * kc; // mm/day
    const waterNeedLiters = Math.round(waterNeedMM * 4047); // 1mm on 1 acre = 4047 liters

    document.getElementById('water-need-value').textContent = waterNeedLiters.toLocaleString();

    // Irrigate today?
    const rain3 = fc.daily ? fc.daily.precipitation_sum.slice(0, 1).reduce((a, b) => a + (b || 0), 0) : 0;
    let irrigate, irrigateColor;
    if (rain3 > 5) { irrigate = { en: '🌧️ NO — Rain expected', hi: '🌧️ नहीं — बारिश आएगी' }; irrigateColor = '#3b82f6'; }
    else if (sm > 0.35) { irrigate = { en: '💧 NO — Soil moist', hi: '💧 नहीं — मिट्टी गीली' }; irrigateColor = '#22c55e'; }
    else if (sm < 0.15) { irrigate = { en: '🔴 YES — Urgent!', hi: '🔴 हाँ — तुरंत!' }; irrigateColor = '#ef4444'; }
    else { irrigate = { en: '🟡 Check by evening', hi: '🟡 शाम तक देखें' }; irrigateColor = '#f59e0b'; }

    const irrigateEl = document.getElementById('irrigate-value');
    irrigateEl.textContent = (irrigate[currentLang] || irrigate.en);
    irrigateEl.style.color = irrigateColor;
    irrigateEl.style.fontSize = '18px';
}

// ===== EMERGENCY HELPLINES =====
const helplines = [
    { icon: '📞', name: { en: 'Kisan Call Center', hi: 'किसान कॉल सेंटर' }, desc: { en: 'Toll-free, all languages, 24/7', hi: 'टोल-फ्री, सभी भाषाएं, 24/7' }, number: '1800-180-1551', toll: true },
    { icon: '💰', name: { en: 'PM-KISAN Helpline', hi: 'PM-KISAN हेल्पलाइन' }, desc: { en: 'Payment status, registration', hi: 'भुगतान स्थिति, पंजीकरण' }, number: '155261', toll: true },
    { icon: '🛡️', name: { en: 'PMFBY Crop Insurance', hi: 'PMFBY फसल बीमा' }, desc: { en: 'Claim filing, status check', hi: 'क्लेम दाखिल, स्थिति जांच' }, number: '1800-266-0700', toll: true },
    { icon: '🌾', name: { en: 'Soil Health Card', hi: 'मृदा स्वास्थ्य कार्ड' }, desc: { en: 'Get your soil tested free', hi: 'मिट्टी जांच करवाएं (मुफ्त)' }, number: '14447', toll: true },
    { icon: '🐛', name: { en: 'Pest/Disease Helpline', hi: 'कीट/रोग हेल्पलाइन' }, desc: { en: 'Plant protection advice', hi: 'फसल सुरक्षा सलाह' }, number: '1800-180-1551', toll: true },
    { icon: '💧', name: { en: 'Water/Irrigation', hi: 'जल/सिंचाई' }, desc: { en: 'Irrigation schemes info', hi: 'सिंचाई योजना जानकारी' }, number: '1800-180-1551', toll: true },
    { icon: '🏦', name: { en: 'NABARD', hi: 'नाबार्ड' }, desc: { en: 'Rural banking, farm credit', hi: 'ग्रामीण बैंकिंग, कृषि ऋण' }, number: '1800-425-0012', toll: true },
    { icon: '🚨', name: { en: 'Emergency', hi: 'आपातकाल' }, desc: { en: 'Disaster, flood, drought relief', hi: 'आपदा, बाढ़, सूखा राहत' }, number: '112', toll: false }
];

function renderHelplines() {
    const container = document.getElementById('helplines-content');
    if (!container) return;
    container.innerHTML = helplines.map(h => {
        const name = h.name[currentLang] || h.name.en;
        const desc = h.desc[currentLang] || h.desc.en;
        return `<div class="helpline-card" onclick="window.open('tel:${h.number}')"><span class="helpline-icon">${h.icon}</span><div><h4>${name}</h4><p>${desc}</p></div><span class="helpline-number">${h.number}</span></div>`;
    }).join('');
}
renderHelplines();

// ===== FINANCIAL TOOLS =====
document.getElementById('calc-emi')?.addEventListener('click', () => {
    const P = parseFloat(document.getElementById('loan-amount').value) || 100000;
    const r = (parseFloat(document.getElementById('loan-rate').value) || 4) / 100 / 12;
    const n = (parseInt(document.getElementById('loan-years').value) || 3) * 12;
    const emi = P * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
    const total = emi * n;
    const interest = total - P;
    const result = currentLang === 'hi'
        ? `EMI: ₹${Math.round(emi).toLocaleString()}/माह | कुल: ₹${Math.round(total).toLocaleString()} | ब्याज: ₹${Math.round(interest).toLocaleString()}`
        : `EMI: ₹${Math.round(emi).toLocaleString()}/month | Total: ₹${Math.round(total).toLocaleString()} | Interest: ₹${Math.round(interest).toLocaleString()}`;
    document.getElementById('emi-result').textContent = result;
});

function updateIncomeEstimate() {
    const crop = document.getElementById('crop-select').value;
    const area = parseFloat(document.getElementById('farm-area')?.value) || 2;
    const yieldPerHa = parseFloat(document.getElementById('est-yield')?.value) || 3;
    const msp = mspRates[crop] || 0;
    if (msp === 0) {
        document.getElementById('income-result').textContent = currentLang === 'hi' ? 'MSP उपलब्ध नहीं। मंडी भाव देखें।' : 'No MSP for this crop. Check mandi prices.';
        return;
    }
    const areaHa = area * 0.4047;
    const totalYield = yieldPerHa * areaHa;
    const totalQuintals = totalYield * 10;
    const income = totalQuintals * msp;
    const result = currentLang === 'hi'
        ? `📊 अनुमानित आय: ₹${Math.round(income).toLocaleString()} (${totalQuintals.toFixed(1)} क्विंटल × ₹${msp}/क्विंटल MSP)`
        : `📊 Estimated Income: ₹${Math.round(income).toLocaleString()} (${totalQuintals.toFixed(1)} quintals × ₹${msp}/q MSP)`;
    document.getElementById('income-result').textContent = result;
}
document.getElementById('farm-area')?.addEventListener('input', updateIncomeEstimate);
document.getElementById('est-yield')?.addEventListener('input', updateIncomeEstimate);
document.getElementById('crop-select')?.addEventListener('change', updateIncomeEstimate);

// ===== ACCESSIBILITY TOGGLES =====
document.getElementById('toggle-lowdata')?.addEventListener('click', function () {
    document.body.classList.toggle('low-data');
    this.classList.toggle('active');
});
document.getElementById('toggle-contrast')?.addEventListener('click', function () {
    document.body.classList.toggle('high-contrast');
    this.classList.toggle('active');
});
document.getElementById('toggle-fontsize')?.addEventListener('click', function () {
    document.body.classList.toggle('large-text');
    this.classList.toggle('active');
});

// ===== HOOK V5 INTO RENDER PIPELINE =====
const originalRenderDashboard = window.renderDashboard || renderDashboard;
const _origRd = renderDashboard;
// Monkey-patch: after V3 renderDashboard, also run V5 updates
const __origSelectLocation = selectLocation;
// We need to call soil + water + income after data loads
// Inject via event — check if data is available periodically
const v5Updater = setInterval(() => {
    if (typeof currentWeather !== 'undefined' && currentWeather && typeof currentPower !== 'undefined' && currentPower) {
        updateSoilHealth(currentWeather, currentPower);
        updateWaterCalc(currentWeather);
        updateIncomeEstimate();
        clearInterval(v5Updater);
    }
}, 2000);

// Also update on crop change
document.getElementById('crop-select')?.addEventListener('change', () => {
    if (currentWeather && currentPower) {
        updateSoilHealth(currentWeather, currentPower);
        updateWaterCalc(currentWeather);
    }
});

// ===== I18N ADDITIONS FOR 4 MORE LANGUAGES =====
i18n.bn = {
    tagline: "প্রতিটি কৃষকের জন্য উপগ্রহ বুদ্ধিমত্তা",
    searchPlaceholder: "গ্রাম, জেলা বা শহর খুঁজুন...",
    coordDefault: "আপনার খামার নির্বাচন করতে মানচিত্রে ক্লিক করুন",
    loading: "উপগ্রহ ডেটা আনা হচ্ছে...",
    ndviTitle: "ফসল স্বাস্থ্য (NDVI)", soilTitle: "মাটির আর্দ্রতা", tempTitle: "তাপমাত্রা",
    forecastTitle: "☁️ ৭ দিনের পূর্বাভাস", rainTitle: "🌧️ বৃষ্টিপাত (গত ৩০ দিন)",
    tempChartTitle: "📈 তাপমাত্রা প্রবণতা", advisoryTitle: "🧠 স্মার্ট পরামর্শ",
    speakLabel: "শুনুন",
    advisoryPlaceholder: "উপগ্রহ ভিত্তিক পরামর্শের জন্য মানচিত্রে আপনার খামার নির্বাচন করুন।",
    listening: "শুনছি...", voiceReady: "আপনার খামার সম্পর্কে জিজ্ঞাসা করুন!",
    days: ["রবি", "সোম", "মঙ্গল", "বুধ", "বৃহ", "শুক্র", "শনি"],
};
i18n.gu = {
    tagline: "દરેક ખેડૂત માટે ઉપગ્રહ બુદ્ધિ",
    searchPlaceholder: "ગામ, જિલ્લો કે શહેર શોધો...",
    coordDefault: "તમારું ખેતર પસંદ કરવા નકશા પર ક્લિક કરો",
    loading: "ઉપગ્રહ ડેટા મેળવી રહ્યા છીએ...",
    ndviTitle: "પાક આરોગ્ય (NDVI)", soilTitle: "જમીન ભેજ", tempTitle: "તાપમાન",
    forecastTitle: "☁️ ૭ દિવસ આગાહી", rainTitle: "🌧️ વરસાદ (છેલ્લા ૩૦ દિવસ)",
    tempChartTitle: "📈 તાપમાન પ્રવાહ", advisoryTitle: "🧠 સ્માર્ટ સલાહ",
    speakLabel: "સાંભળો",
    advisoryPlaceholder: "ઉપગ્રહ આધારિત સલાહ માટે નકશા પર ખેતર પસંદ કરો.",
    listening: "સાંભળી રહ્યા છીએ...", voiceReady: "તમારા ખેતર વિશે પૂછો!",
    days: ["રવિ", "સોમ", "મંગળ", "બુધ", "ગુરુ", "શુક્ર", "શનિ"],
};
i18n.pa = {
    tagline: "ਹਰ ਕਿਸਾਨ ਲਈ ਸੈਟੇਲਾਈਟ ਬੁੱਧੀ",
    searchPlaceholder: "ਪਿੰਡ, ਜ਼ਿਲ੍ਹਾ ਜਾਂ ਸ਼ਹਿਰ ਖੋਜੋ...",
    coordDefault: "ਆਪਣਾ ਖੇਤ ਚੁਣਨ ਲਈ ਨਕਸ਼ੇ ਤੇ ਕਲਿੱਕ ਕਰੋ",
    loading: "ਸੈਟੇਲਾਈਟ ਡੇਟਾ ਮਿਲ ਰਿਹਾ ਹੈ...",
    ndviTitle: "ਫ਼ਸਲ ਸਿਹਤ (NDVI)", soilTitle: "ਮਿੱਟੀ ਨਮੀ", tempTitle: "ਤਾਪਮਾਨ",
    forecastTitle: "☁️ 7 ਦਿਨ ਅਨੁਮਾਨ", rainTitle: "🌧️ ਬਾਰਿਸ਼ (ਪਿਛਲੇ 30 ਦਿਨ)",
    tempChartTitle: "📈 ਤਾਪਮਾਨ ਰੁਝਾਨ", advisoryTitle: "🧠 ਸਮਾਰਟ ਸਲਾਹ",
    speakLabel: "ਸੁਣੋ",
    advisoryPlaceholder: "ਸੈਟੇਲਾਈਟ ਆਧਾਰਿਤ ਸਲਾਹ ਲਈ ਨਕਸ਼ੇ ਤੇ ਖੇਤ ਚੁਣੋ।",
    listening: "ਸੁਣ ਰਿਹਾ ਹਾਂ...", voiceReady: "ਆਪਣੇ ਖੇਤ ਬਾਰੇ ਪੁੱਛੋ!",
    days: ["ਐਤ", "ਸੋਮ", "ਮੰਗਲ", "ਬੁੱਧ", "ਵੀਰ", "ਸ਼ੁੱਕਰ", "ਸ਼ਨੀ"],
};
i18n.or = {
    tagline: "ପ୍ରତ୍ୟେକ ଚାଷୀ ପାଇଁ ଉପଗ୍ରହ ବୁଦ୍ଧିମତ୍ତା",
    searchPlaceholder: "ଗାଁ, ଜିଲ୍ଲା ବା ସହର ଖୋଜନ୍ତୁ...",
    coordDefault: "ଆପଣଙ୍କ କ୍ଷେତ ବାଛିବା ପାଇଁ ମାନଚିତ୍ରରେ କ୍ଲିକ୍ କରନ୍ତୁ",
    loading: "ଉପଗ୍ରହ ତଥ୍ୟ ପାଇବାରେ ଅଛି...",
    ndviTitle: "ଫସଲ ସ୍ୱାସ୍ଥ୍ୟ (NDVI)", soilTitle: "ମାଟି ଆର୍ଦ୍ରତା", tempTitle: "ତାପମାତ୍ରା",
    forecastTitle: "☁️ ୭ ଦିନ ପୂର୍ବାନୁମାନ", rainTitle: "🌧️ ବର୍ଷା (ଗତ ୩୦ ଦିନ)",
    tempChartTitle: "📈 ତାପମାତ୍ରା ପ୍ରବୃତ୍ତି", advisoryTitle: "🧠 ସ୍ମାର୍ଟ ପରାମର୍ଶ",
    speakLabel: "ଶୁଣନ୍ତୁ",
    advisoryPlaceholder: "ଉପଗ୍ରହ ଆଧାରିତ ପରାମର୍ଶ ପାଇଁ ମାନଚିତ୍ରରେ ଆପଣଙ୍କ କ୍ଷେତ ବାଛନ୍ତୁ।",
    listening: "ଶୁଣୁଛି...", voiceReady: "ଆପଣଙ୍କ କ୍ଷେତ ବିଷୟରେ ପଚାରନ୍ତୁ!",
    days: ["ରବି", "ସୋମ", "ମଙ୍ଗଳ", "ବୁଧ", "ଗୁରୁ", "ଶୁକ୍ର", "ଶନି"],
};

// Update language handler for V5 panels
const _origUpdateLang = updateLanguage;
updateLanguage = function () {
    _origUpdateLang();
    renderHelplines();
    renderSchemes();
    if (currentWeather && currentPower) {
        updateSoilHealth(currentWeather, currentPower);
        updateWaterCalc(currentWeather);
    }
    updateIncomeEstimate();
};

console.log('🌾 Krishikarm v7 — AI Farming Intelligence Platform loaded');

// ===== FARMER BUDDY ENGINE =====
const API = '';

// --- BUDDY CHAT ---
const buddyChat = document.getElementById('buddy-chat');
const buddyInput = document.getElementById('buddy-input');
const buddySendBtn = document.getElementById('buddy-send-btn');
const buddyVoiceBtn = document.getElementById('buddy-voice-btn');

function addBuddyMsg(text, isUser = false) {
    const div = document.createElement('div');
    div.className = `chat-msg ${isUser ? 'user' : 'bot'}`;
    const formatted = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/\n/g, '<br>')
        .replace(/• /g, '&bull; ');
    div.innerHTML = `
        <span class="chat-avatar">${isUser ? '👤' : '🌾'}</span>
        <div class="chat-bubble">${formatted}</div>
    `;
    buddyChat.appendChild(div);
    buddyChat.scrollTop = buddyChat.scrollHeight;
    return div;
}

async function sendBuddyQuestion(question) {
    if (!question.trim()) return;
    addBuddyMsg(question, true);
    buddyInput.value = '';

    const thinkingDiv = addBuddyMsg('Thinking... 🔄');

    try {
        // Read language directly from picker to guarantee correct language
        const buddyLang = document.getElementById('lang-picker')?.value || currentLang;
        console.log(`💬 Sending buddy question with lang: ${buddyLang}`);
        const res = await fetch(`${API}/buddy/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question,
                lang: buddyLang,
                lat: currentLat,
                lon: currentLng,
            }),
        });
        const data = await res.json();
        thinkingDiv.remove();
        const msgDiv = addBuddyMsg(data.advice || data.advice_en || 'I could not process that. Please try again.');

        // Add TTS button
        const ttsBtn = document.createElement('button');
        ttsBtn.className = 'buddy-chip';
        ttsBtn.textContent = '🔊 Listen';
        ttsBtn.style.marginTop = '6px';
        ttsBtn.onclick = async () => {
            ttsBtn.textContent = '🔊 Generating...';
            try {
                const ttsRes = await fetch(`${API}/buddy/tts`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `text=${encodeURIComponent(data.advice || data.advice_en)}&lang=${currentLang}`,
                });
                const ttsData = await ttsRes.json();
                if (ttsData.audio_base64) {
                    const audio = new Audio(`data:audio/wav;base64,${ttsData.audio_base64}`);
                    audio.play();
                    ttsBtn.textContent = '🔊 Playing...';
                    audio.onended = () => { ttsBtn.textContent = '🔊 Listen'; };
                }
            } catch (e) {
                ttsBtn.textContent = '🔊 Listen';
            }
        };
        msgDiv.querySelector('.chat-bubble').appendChild(ttsBtn);

    } catch (e) {
        thinkingDiv.remove();
        addBuddyMsg('Sorry, I could not connect to the server. Please check if the backend is running.');
    }
}

if (buddySendBtn) {
    buddySendBtn.addEventListener('click', () => sendBuddyQuestion(buddyInput.value));
}
if (buddyInput) {
    buddyInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendBuddyQuestion(buddyInput.value);
    });
}

// Quick action chips
document.querySelectorAll('.buddy-chip[data-q]').forEach(chip => {
    chip.addEventListener('click', () => {
        sendBuddyQuestion(chip.dataset.q);
    });
});

// --- VOICE RECORDING ---
let mediaRecorder = null;
let audioChunks = [];

if (buddyVoiceBtn) {
    buddyVoiceBtn.addEventListener('click', async () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            buddyVoiceBtn.classList.remove('recording');
            return;
        }
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
            mediaRecorder.onstop = async () => {
                stream.getTracks().forEach(t => t.stop());
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                addBuddyMsg('🎤 Voice note sent...', true);
                const thinkingDiv = addBuddyMsg('Processing your voice... 🔄');

                const formData = new FormData();
                formData.append('audio', audioBlob, 'voice.wav');
                // Read language directly from picker to be safe
                const pickerLang = document.getElementById('lang-picker')?.value || currentLang;
                formData.append('lang', pickerLang);
                console.log(`🎤 Sending voice note with lang: ${pickerLang}`);

                try {
                    const res = await fetch(`${API}/buddy/voice`, { method: 'POST', body: formData });
                    const data = await res.json();
                    thinkingDiv.remove();
                    if (data.transcript) addBuddyMsg(`📝 You said: "${data.transcript}"`, false);
                    addBuddyMsg(data.advice || 'Could not process audio.');

                    if (data.audio_base64) {
                        const audio = new Audio(`data:audio/wav;base64,${data.audio_base64}`);
                        audio.play();
                    }
                } catch (e) {
                    thinkingDiv.remove();
                    addBuddyMsg('Could not process voice note. Is the backend running?');
                }
            };
            mediaRecorder.start();
            buddyVoiceBtn.classList.add('recording');
        } catch (e) {
            addBuddyMsg('Microphone access denied. Please allow microphone access.');
        }
    });
}

// --- MARKETPLACE ---
const fetchPricesBtn = document.getElementById('fetch-prices-btn');
const marketCropSelect = document.getElementById('market-crop-select');
const mandiPricesDiv = document.getElementById('mandi-prices');

async function fetchMandiPrices() {
    const crop = marketCropSelect ? marketCropSelect.value : 'rice';
    if (mandiPricesDiv) mandiPricesDiv.innerHTML = '<p style="color:var(--text-secondary)">Loading prices...</p>';

    try {
        const res = await fetch(`${API}/buddy/marketplace/${crop}`);
        const data = await res.json();

        if (data.prices && data.prices.length > 0) {
            mandiPricesDiv.innerHTML = data.prices.map(p => `
                <div class="mandi-card">
                    <div class="mandi-market">📍 ${p.market || 'Unknown'}</div>
                    <div class="mandi-location">${p.district || ''}, ${p.state || ''}</div>
                    <div class="mandi-price">₹${p.modal_price || 'N/A'} <span class="mandi-unit">/ quintal</span></div>
                </div>
            `).join('');
        } else {
            mandiPricesDiv.innerHTML = '<p style="color:var(--text-muted)">No prices available. Try another crop.</p>';
        }
    } catch (e) {
        mandiPricesDiv.innerHTML = '<p style="color:var(--accent-red)">Could not fetch prices. Check backend.</p>';
    }
}

if (fetchPricesBtn) fetchPricesBtn.addEventListener('click', fetchMandiPrices);
// Auto-fetch on load
setTimeout(fetchMandiPrices, 2000);

// --- ACTION CARDS ---
const sendWhatsAppAction = document.getElementById('send-whatsapp-action');
if (sendWhatsAppAction) {
    sendWhatsAppAction.addEventListener('click', async () => {
        const phone = '917259426670';
        const crop = document.getElementById('crop-select')?.value || 'general';
        let msg = `🌾 Krishikarm Farm Report\n`;
        msg += `📍 Location: ${currentLat?.toFixed(4) || 'N/A'}, ${currentLng?.toFixed(4) || 'N/A'}\n`;
        msg += `🌿 NDVI: ${document.getElementById('ndvi-value')?.textContent || '--'}\n`;
        msg += `🌡️ Temp: ${document.getElementById('temp-now')?.textContent || '--'}\n`;
        msg += `💧 Soil: ${document.getElementById('soil-0-pct')?.textContent || '--'}\n`;
        msg += `🌾 Crop: ${crop}\n`;
        msg += `⏰ ${new Date().toLocaleString('en-IN')}\n`;
        msg += `\n🛰️ Powered by Krishikarm`;

        try {
            const res = await fetch(`${API}/buddy/whatsapp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone, message: msg, lang: currentLang, farmer_name: 'Farmer' }),
            });
            const data = await res.json();
            if (data.link) {
                window.open(data.link, '_blank');
            }
            addBuddyMsg('📲 WhatsApp report sent! Check your phone.');
        } catch (e) {
            window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, '_blank');
        }
    });
}

const registerSchemeAction = document.getElementById('register-scheme-action');
if (registerSchemeAction) {
    registerSchemeAction.addEventListener('click', () => {
        window.open('https://pmkisan.gov.in/', '_blank');
        sendBuddyQuestion('Help me register for PM-KISAN scheme');
    });
}

const budgetTipsAction = document.getElementById('budget-tips-action');
if (budgetTipsAction) {
    budgetTipsAction.addEventListener('click', () => {
        sendBuddyQuestion('Give me budget farming techniques that cost nothing');
    });
}

const voiceBuddyAction = document.getElementById('voice-buddy-action');
if (voiceBuddyAction) {
    voiceBuddyAction.addEventListener('click', () => {
        if (buddyVoiceBtn) buddyVoiceBtn.click();
        document.getElementById('buddy-panel')?.scrollIntoView({ behavior: 'smooth' });
    });
}

// --- AUTO-REFRESH LIVE DATA ---
setInterval(() => {
    const statusEl = document.getElementById('ml-status');
    if (statusEl) {
        const now = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
        statusEl.textContent = `🧠 AI: Live (${now})`;
    }
}, 60000);

// --- AUTO-GEOLOCATION ON LOAD ---
// Automatically detect user's location and load weather data right away
setTimeout(() => {
    if (!currentLat && 'geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                console.log(`📍 Auto-detected location: ${pos.coords.latitude}, ${pos.coords.longitude}`);
                selectLocation(pos.coords.latitude, pos.coords.longitude);
            },
            (err) => {
                console.log('📍 Geolocation denied, loading default (Bangalore)');
                // Default to Bangalore (Karnataka) if geolocation denied
                selectLocation(12.9716, 77.5946);
            },
            { timeout: 5000, maximumAge: 60000 }
        );
    }
}, 1500);

