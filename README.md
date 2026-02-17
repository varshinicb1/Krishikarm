# Krishikarm

**AI-powered farming intelligence platform combining satellite data with voice AI.**

Krishikarm provides personalized agricultural advice to Indian farmers through
real-time satellite analysis, multilingual voice interaction, and live market prices.
The platform is built around KisanNet v3, a cross-attention transformer trained on
82,000+ real satellite observations across 127 Indian districts with 96.8% accuracy.

---

## Features

### KisanNet v3 (Trained Model)

- Cross-attention transformer with 42 input features
- Trained on real satellite data from NASA POWER, Open-Meteo, and SoilGrids
- Predicts crop distress score, intervention window, and 5-level risk classification
- Inference time: ~4ms on GPU
- Available as a standalone Python package: `pip install krishikarm`

### Voice-First Interface

- Speech-to-text and text-to-speech powered by Sarvam AI
- Supports 11 Indian languages: Hindi, Kannada, Telugu, Tamil, Marathi, Bengali,
  Gujarati, Punjabi, Odia, Malayalam, and English
- Designed for accessibility in rural areas

### Satellite Intelligence

- Real-time data fusion from NASA GIBS, ISRO Bhuvan, Open-Meteo, and SoilGrids
- Visual map layers: NDVI (crop health), soil moisture, temperature, true color

### Krishikarm Buddy

- Context-aware AI assistant for farming queries
- Knows your farm location, soil type, and weather forecast
- WhatsApp integration for sending reports and advisories

### Mandi Marketplace

- Real-time commodity prices from data.gov.in (AgMarkNet)
- Covers all major agricultural markets across India

---

## Tech Stack

| Layer     | Technologies                                                    |
|-----------|-----------------------------------------------------------------|
| Frontend  | Vite, Vanilla JS, Leaflet, Chart.js, TensorFlow.js             |
| Backend   | FastAPI, Python, SQLite, Sarvam AI                              |
| AI/ML     | PyTorch (training), ONNX (inference), Transformer architecture  |
| Data      | NASA POWER, ISRO Bhuvan, Open-Meteo, AgMarkNet, SoilGrids      |

---

## Setup

### Prerequisites

- Node.js (v18+)
- Python (v3.9+)

### 1. Clone

```bash
git clone https://github.com/varshinicb1/Krishikarm.git
cd Krishikarm
```

### 2. Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set SARVAM_API_KEY and MANDI_API_KEY

python server.py
```

### 3. Frontend

```bash
npm install
npm run dev
```

The backend runs at `http://localhost:8000`, the frontend at `http://localhost:5173`.

---

## Python Package

The trained model is also available as a standalone package:

```bash
pip install krishikarm
```

```python
from krishikarm import Predictor

p = Predictor()
result = p.predict({
    "lat": 12.97, "lon": 77.59,
    "T2M": 32, "RH2M": 65, "PREC": 2.5,
    "state": "KA", "irrig": "borewell",
    "crops": ["rice"],
})
print(result["risk_label"])  # "Healthy"
```

See [PKG_README.md](PKG_README.md) for full API documentation.

---

## Environment Variables

| Variable         | Description                          | Required |
|------------------|--------------------------------------|----------|
| `SARVAM_API_KEY` | Sarvam AI key for voice/translation  | Yes      |
| `MANDI_API_KEY`  | data.gov.in key for market prices    | Yes      |

---

## License

MIT. See [LICENSE](LICENSE) for details.
