
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

console.log('🛰️ Kisan-Eye V5 — Universal Farmer Platform loaded');
