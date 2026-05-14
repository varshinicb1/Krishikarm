/**
 * Kisan-Eye V6 — Kiosk Mode Controller
 * Camera → Face Recognition → AI Chat → Voice
 * All functions attached to window for inline onclick compatibility (Vite IIFE)
 */

const BACKEND_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : `${window.location.protocol}//${window.location.hostname}:8000`;

let kioskActive = false;
let currentFarmerId = localStorage.getItem('krishikarm_farmer_id');
let currentToken = localStorage.getItem('krishikarm_token');
let videoStream = null;
let capturedImageBlob = null;

// ===== KIOSK TOGGLE =====
window.toggleKiosk = function () {
    const overlay = document.getElementById('kiosk-overlay');
    kioskActive = !kioskActive;

    if (kioskActive) {
        overlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        startCamera();
    } else {
        overlay.style.display = 'none';
        document.body.style.overflow = '';
        stopCamera();
    }
}

// Add kiosk button to header — runs immediately if DOM is ready, otherwise waits
function _addKioskButton() {
    if (document.getElementById('kiosk-mode-btn')) return;
    const header = document.querySelector('.header-controls') || document.querySelector('header');
    if (header) {
        const btn = document.createElement('button');
        btn.id = 'kiosk-mode-btn';
        btn.className = 'accessibility-btn';
        btn.title = 'Kiosk Mode';
        btn.textContent = '🏛️';
        btn.onclick = window.toggleKiosk;
        btn.style.cssText = 'font-size:20px;padding:6px 12px;cursor:pointer;border:1px solid rgba(255,255,255,0.3);border-radius:8px;background:rgba(34,197,94,0.2);margin-left:8px;';
        header.appendChild(btn);
    }
}
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', _addKioskButton);
} else {
    _addKioskButton();
}

// ===== CAMERA =====
async function startCamera() {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480, facingMode: 'user' }
        });
        const video = document.getElementById('kiosk-video');
        video.srcObject = videoStream;
        document.getElementById('kiosk-camera-status').textContent = '📷 Camera active — Show your face';
    } catch (e) {
        document.getElementById('kiosk-camera-status').textContent = '❌ Camera error: ' + e.message;
    }
}

function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(t => t.stop());
        videoStream = null;
    }
}

// ===== FACE IDENTIFICATION =====
window.captureAndIdentify = async function () {
    const video = document.getElementById('kiosk-video');
    const canvas = document.getElementById('kiosk-canvas');
    const status = document.getElementById('kiosk-camera-status');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    status.textContent = '🔍 Identifying...';

    // Convert to blob
    const blob = await new Promise(r => canvas.toBlob(r, 'image/jpeg', 0.9));
    capturedImageBlob = blob;

    // SIMULATED MOCK API FOR SERVERLESS
    setTimeout(() => {
        const mockData = {
            status: 'identified',
            farmer_id: 'FARMER_001',
            token: 'mock_token',
            confidence: 0.95,
            farmer: {
                name: 'Ramesh Kumar',
                village: 'Navalur',
                district: 'Dharwad',
                state: 'Karnataka',
                language: 'kn',
                land_acres: 5,
                crops: ['Cotton', 'Maize'],
                irrigation_type: 'Rain-fed',
                financial_state: 'Stable',
                family_members: 6,
                bpl_card: true
            }
        };

        currentFarmerId = mockData.farmer_id;
        currentToken = mockData.token;
        localStorage.setItem('krishikarm_farmer_id', currentFarmerId);
        localStorage.setItem('krishikarm_token', currentToken);
        status.textContent = `✅ Welcome back, ${mockData.farmer.name}! (${(mockData.confidence * 100).toFixed(0)}% match)`;
        status.style.color = '#22c55e';
        showFarmerProfile(mockData.farmer);
        loadSchemes(mockData.farmer_id);
        loadFarmData(mockData.farmer_id);
        addChatMessage('bot', `Namaste ${mockData.farmer.name}! 🙏 Welcome back. How can I help you today? Ask me about your farm, weather, schemes, or any question.`);
    }, 1500);
}

// ===== FARMER PROFILE =====
function showFarmerProfile(farmer) {
    const info = document.getElementById('kiosk-farmer-info');
    const lang = farmer.language || 'hi';

    info.innerHTML = `
    <div class="profile-grid">
      <div class="profile-item"><strong>👤 Name:</strong> ${farmer.name}</div>
      <div class="profile-item"><strong>🏘️ Village:</strong> ${farmer.village || '--'}, ${farmer.district || ''}</div>
      <div class="profile-item"><strong>📍 State:</strong> ${farmer.state || '--'}</div>
      <div class="profile-item"><strong>🌐 Language:</strong> ${lang.toUpperCase()}</div>
      <div class="profile-item"><strong>🌾 Land:</strong> ${farmer.land_acres || 0} acres</div>
      <div class="profile-item"><strong>🌱 Crops:</strong> ${(farmer.crops || []).join(', ') || 'Not set'}</div>
      <div class="profile-item"><strong>💧 Irrigation:</strong> ${farmer.irrigation_type || 'Rain-fed'}</div>
      <div class="profile-item"><strong>💰 Financial:</strong> ${farmer.financial_state || 'Stable'}</div>
      <div class="profile-item"><strong>👨‍👩‍👧‍👦 Family:</strong> ${farmer.family_members || 4} members</div>
      ${farmer.bpl_card ? '<div class="profile-item"><strong>📋 BPL:</strong> Yes</div>' : ''}
    </div>
  `;
}

// ===== LOAD SCHEMES =====
async function loadSchemes(farmerId) {
    // SIMULATED MOCK API
    setTimeout(() => {
        const mockSchemes = [
            { name: 'PM-KISAN', benefit: '₹6000/year', reason: 'You own < 5 acres', helpline: '155261' },
            { name: 'Fasal Bima Yojana', benefit: 'Crop Insurance', reason: 'Protects your Cotton', helpline: '14447' }
        ];

        const container = document.getElementById('kiosk-schemes-list');
        const panel = document.getElementById('kiosk-schemes');
        panel.style.display = 'block';

        container.innerHTML = '';
        mockSchemes.forEach(s => {
            const item = document.createElement('div');
            item.className = 'scheme-item';
            
            const name = document.createElement('div');
            name.className = 'scheme-name';
            name.textContent = s.name;
            
            const benefit = document.createElement('div');
            benefit.className = 'scheme-benefit';
            benefit.textContent = s.benefit;
            
            const meta = document.createElement('div');
            meta.className = 'scheme-meta';
            
            const reason = document.createElement('span');
            reason.textContent = s.reason;
            
            const call = document.createElement('a');
            call.href = `tel:${s.helpline}`;
            call.className = 'scheme-call';
            call.textContent = `📞 ${s.helpline}`;
            
            meta.appendChild(reason);
            meta.appendChild(call);
            item.appendChild(name);
            item.appendChild(benefit);
            item.appendChild(meta);
            container.appendChild(item);
        });
    }, 1000);
}

// ===== LOAD FARM DATA =====
async function loadFarmData(farmerId) {
    // SIMULATED MOCK API
    setTimeout(() => {
        const fd = {
            temperature: 28,
            humidity: 65,
            ndvi: 0.65,
            ndvi_label: 'Healthy',
            soil_moisture: 0.45,
            rainfall_7d: 12,
            irrigate_decision: 'NO - Soil is moist'
        };

        const container = document.getElementById('kiosk-sat-data');
        const panel = document.getElementById('kiosk-farm-data');
        panel.style.display = 'block';

        container.innerHTML = '';
        const grid = document.createElement('div');
        grid.className = 'sat-grid';
        
        const metrics = [
            { label: '🌡️ Temp', value: `${fd.temperature || '--'}°C` },
            { label: '💧 Humidity', value: `${fd.humidity || '--'}%` },
            { label: '🌱 NDVI', value: `${fd.ndvi || '--'} (${fd.ndvi_label || ''})` },
            { label: '🌊 Soil Moisture', value: fd.soil_moisture ? (fd.soil_moisture * 100).toFixed(0) + '%' : '--' },
            { label: '🌧️ Rain (7d)', value: `${fd.rainfall_7d || 0} mm` },
            { label: '💧 Irrigate?', value: fd.irrigate_decision || '--', color: fd.irrigate_decision?.includes('YES') ? '#ef4444' : '#22c55e' }
        ];
        
        metrics.forEach(m => {
            const item = document.createElement('div');
            item.className = 'sat-item';
            const lbl = document.createElement('span');
            lbl.textContent = m.label;
            const val = document.createElement('strong');
            val.textContent = m.value;
            if (m.color) val.style.color = m.color;
            item.appendChild(lbl);
            item.appendChild(val);
            grid.appendChild(item);
        });
        container.appendChild(grid);
    }, 1000);
}

// ===== AI CHAT =====
window.kioskSendMessage = async function () {
    const input = document.getElementById('kiosk-chat-input');
    const query = input.value.trim();
    if (!query) return;

    addChatMessage('user', query);
    input.value = '';

    if (!currentFarmerId) {
        addChatMessage('bot', 'Please identify yourself first by showing your face to the camera, or register as a new farmer.');
        return;
    }

    addChatMessage('bot', '⏳ Thinking...');

    setTimeout(() => {
        // Remove "thinking" message
        const messages = document.getElementById('kiosk-chat-messages');
        const last = messages.lastElementChild;
        if (last && last.textContent.includes('Thinking')) last.remove();

        let mockResponse = "Namaskara! This is the Krishikarm Kiosk Buddy. Since we are in offline mode, I recommend checking your crop calendar above for immediate actions.";
        if (query.toLowerCase().includes("cotton")) mockResponse = "For cotton, ensure you spray Neem oil at early growth stages to prevent bollworm attacks.";
        
        addChatMessage('bot', mockResponse);

        // Auto-speak the response
        if ('speechSynthesis' in window) {
            const u = new SpeechSynthesisUtterance(mockResponse);
            u.lang = 'hi-IN';
            u.rate = 0.85;
            window.speechSynthesis.speak(u);
        }
    }, 1200);
}

function addChatMessage(role, text) {
    const container = document.getElementById('kiosk-chat-messages');
    if (!container) return;
    const div = document.createElement('div');
    div.className = `chat-message ${role}`;
    const p = document.createElement('p');
    p.textContent = text;
    div.appendChild(p);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// Enter key sends message
document.getElementById('kiosk-chat-input')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') window.kioskSendMessage();
});

// ===== VOICE INPUT =====
window.kioskVoiceInput = function () {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        addChatMessage('bot', 'Voice input not supported in this browser. Please type your question.');
        return;
    }

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SR();
    recognition.lang = 'hi-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    const status = document.getElementById('kiosk-voice-status');
    status.style.display = 'block';
    document.getElementById('kiosk-voice-btn').style.background = '#ef4444';

    recognition.start();

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        document.getElementById('kiosk-chat-input').value = text;
        status.style.display = 'none';
        document.getElementById('kiosk-voice-btn').style.background = '';
        kioskSendMessage();
    };

    recognition.onerror = () => {
        status.style.display = 'none';
        document.getElementById('kiosk-voice-btn').style.background = '';
    };

    recognition.onend = () => {
        status.style.display = 'none';
        document.getElementById('kiosk-voice-btn').style.background = '';
    };
}

// ===== REGISTRATION =====
window.registerFarmer = async function () {
    if (!capturedImageBlob) {
        alert('Please capture your face first!');
        return;
    }

    setTimeout(() => {
        const mockData = {
            status: 'registered',
            farmer_id: 'NEW_FARMER_123',
            token: 'mock_token_new',
            farmer: {
                name: document.getElementById('reg-name').value || 'New Farmer',
                village: document.getElementById('reg-village').value || 'Unknown',
                district: document.getElementById('reg-district').value || 'Unknown',
                state: document.getElementById('reg-state').value || 'Unknown',
                language: document.getElementById('reg-lang').value || 'hi',
                land_acres: parseFloat(document.getElementById('reg-land').value) || 0,
                crops: document.getElementById('reg-crops').value.split(',').map(c => c.trim()).filter(Boolean),
                irrigation_type: document.getElementById('reg-irrigation').value || 'Rain-fed',
                financial_state: 'Stable',
                family_members: 4,
                bpl_card: false
            }
        };

        currentFarmerId = mockData.farmer_id;
        currentToken = mockData.token;
        localStorage.setItem('krishikarm_farmer_id', currentFarmerId);
        localStorage.setItem('krishikarm_token', currentToken);
        document.getElementById('kiosk-register-form').style.display = 'none';
        document.getElementById('kiosk-camera-status').textContent = `✅ Registered! Welcome, ${mockData.farmer.name}!`;
        document.getElementById('kiosk-camera-status').style.color = '#22c55e';
        showFarmerProfile(mockData.farmer);
        loadSchemes(mockData.farmer_id);
        addChatMessage('bot', `Welcome ${mockData.farmer.name}! 🎉 You are now registered. Ask me anything about farming, schemes, or weather.`);
    }, 1500);
}

// ===== DEMO MODE (when backend not available) =====
function showDemoMode() {
    const demoFarmer = {
        name: 'Demo Farmer',
        village: 'Sample Village',
        district: 'Sample District',
        state: 'Karnataka',
        language: 'kn',
        land_acres: 3,
        crops: ['rice', 'jowar'],
        irrigation_type: 'rainfed',
        financial_state: 'stable',
        family_members: 5,
        bpl_card: false
    };
    showFarmerProfile(demoFarmer);
    addChatMessage('bot', '⚠️ Demo mode: Backend server not connected. Start the backend with:\n\ncd backend && python server.py\n\nThen refresh this page.');
}

console.log('🏛️ Kiosk Mode loaded — Click 🏛️ to enter kiosk view');
