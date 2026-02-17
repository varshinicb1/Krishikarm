/**
 * Kisan-Eye V6 — Kiosk Mode Controller
 * Camera → Face Recognition → AI Chat → Voice
 * All functions attached to window for inline onclick compatibility (Vite IIFE)
 */

const BACKEND_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : `${window.location.protocol}//${window.location.hostname}:8000`;

let kioskActive = false;
let currentFarmerId = null;
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

    const formData = new FormData();
    formData.append('image', blob, 'face.jpg');

    try {
        const resp = await fetch(`${BACKEND_URL}/identify`, { method: 'POST', body: formData });
        const data = await resp.json();

        if (data.status === 'identified') {
            currentFarmerId = data.farmer_id;
            status.textContent = `✅ Welcome back, ${data.farmer.name}! (${(data.confidence * 100).toFixed(0)}% match)`;
            status.style.color = '#22c55e';
            showFarmerProfile(data.farmer);
            loadSchemes(data.farmer_id);
            loadFarmData(data.farmer_id);
            addChatMessage('bot', `Namaste ${data.farmer.name}! 🙏 Welcome back. How can I help you today? Ask me about your farm, weather, schemes, or any question.`);
        } else if (data.status === 'unknown') {
            status.textContent = '❓ Face not recognized — Please register below';
            status.style.color = '#f59e0b';
            document.getElementById('kiosk-register-form').style.display = 'block';
        } else if (data.status === 'no_face') {
            status.textContent = '📷 No face detected — Please look directly at the camera';
            status.style.color = '#ef4444';
        } else {
            status.textContent = data.message || 'Please try again';
        }
    } catch (e) {
        // Backend might not be running yet — show demo mode
        status.textContent = '⚠️ Backend not connected — Running in demo mode';
        status.style.color = '#f59e0b';
        showDemoMode();
    }
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
    try {
        const resp = await fetch(`${BACKEND_URL}/schemes/${farmerId}`);
        const data = await resp.json();

        const container = document.getElementById('kiosk-schemes-list');
        const panel = document.getElementById('kiosk-schemes');
        panel.style.display = 'block';

        container.innerHTML = data.schemes.map(s => `
      <div class="scheme-item">
        <div class="scheme-name">${s.name}</div>
        <div class="scheme-benefit">${s.benefit}</div>
        <div class="scheme-meta">
          <span>${s.reason}</span>
          <a href="tel:${s.helpline}" class="scheme-call">📞 ${s.helpline}</a>
        </div>
      </div>
    `).join('');
    } catch (e) {
        console.warn('Schemes fetch failed:', e);
    }
}

// ===== LOAD FARM DATA =====
async function loadFarmData(farmerId) {
    try {
        const resp = await fetch(`${BACKEND_URL}/farm-data/${farmerId}`);
        const data = await resp.json();
        const fd = data.farm_data;

        const container = document.getElementById('kiosk-sat-data');
        const panel = document.getElementById('kiosk-farm-data');
        panel.style.display = 'block';

        container.innerHTML = `
      <div class="sat-grid">
        <div class="sat-item"><span>🌡️ Temp</span><strong>${fd.temperature || '--'}°C</strong></div>
        <div class="sat-item"><span>💧 Humidity</span><strong>${fd.humidity || '--'}%</strong></div>
        <div class="sat-item"><span>🌱 NDVI</span><strong>${fd.ndvi || '--'} (${fd.ndvi_label || ''})</strong></div>
        <div class="sat-item"><span>🌊 Soil Moisture</span><strong>${fd.soil_moisture ? (fd.soil_moisture * 100).toFixed(0) + '%' : '--'}</strong></div>
        <div class="sat-item"><span>🌧️ Rain (7d)</span><strong>${fd.rainfall_7d || 0} mm</strong></div>
        <div class="sat-item"><span>💧 Irrigate?</span><strong style="color:${fd.irrigate_decision?.includes('YES') ? '#ef4444' : '#22c55e'}">${fd.irrigate_decision || '--'}</strong></div>
      </div>
    `;
    } catch (e) {
        console.warn('Farm data fetch failed:', e);
    }
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

    try {
        const resp = await fetch(`${BACKEND_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                farmer_id: currentFarmerId,
                query: query,
                language: 'hi',
                mode: 'text'
            })
        });
        const data = await resp.json();

        // Remove "thinking" message
        const messages = document.getElementById('kiosk-chat-messages');
        const last = messages.lastElementChild;
        if (last && last.textContent.includes('Thinking')) last.remove();

        addChatMessage('bot', data.response);

        // Auto-speak the response
        if ('speechSynthesis' in window) {
            const u = new SpeechSynthesisUtterance(data.response);
            u.lang = 'hi-IN';
            u.rate = 0.85;
            window.speechSynthesis.speak(u);
        }
    } catch (e) {
        const messages = document.getElementById('kiosk-chat-messages');
        const last = messages.lastElementChild;
        if (last && last.textContent.includes('Thinking')) last.remove();
        addChatMessage('bot', 'Sorry, I could not connect to the AI backend. Please try again.');
    }
}

function addChatMessage(role, text) {
    const container = document.getElementById('kiosk-chat-messages');
    const div = document.createElement('div');
    div.className = `chat-message ${role}`;
    div.innerHTML = `<p>${text}</p>`;
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

    const formData = new FormData();
    formData.append('image', capturedImageBlob, 'face.jpg');
    formData.append('data', JSON.stringify({
        name: document.getElementById('reg-name').value,
        village: document.getElementById('reg-village').value,
        district: document.getElementById('reg-district').value,
        state: document.getElementById('reg-state').value,
        language: document.getElementById('reg-lang').value,
        phone: document.getElementById('reg-phone').value,
        land_acres: parseFloat(document.getElementById('reg-land').value) || 0,
        crops: document.getElementById('reg-crops').value.split(',').map(c => c.trim()).filter(Boolean),
        irrigation_type: document.getElementById('reg-irrigation').value,
    }));

    try {
        const resp = await fetch(`${BACKEND_URL}/register`, { method: 'POST', body: formData });
        const data = await resp.json();

        if (data.status === 'registered') {
            currentFarmerId = data.farmer_id;
            document.getElementById('kiosk-register-form').style.display = 'none';
            document.getElementById('kiosk-camera-status').textContent = `✅ Registered! Welcome, ${data.farmer.name}!`;
            document.getElementById('kiosk-camera-status').style.color = '#22c55e';
            showFarmerProfile(data.farmer);
            loadSchemes(data.farmer_id);
            addChatMessage('bot', `Welcome ${data.farmer.name}! 🎉 You are now registered. Ask me anything about farming, schemes, or weather.`);
        }
    } catch (e) {
        alert('Registration failed. Please check if the backend is running.');
    }
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
