# Krishikarm: AI-Powered Agriculture Monitoring System

## 1) Complete System Architecture

Krishikarm is designed as a **multi-layer, closed-loop decision system** where remote sensing, in-field sensing, edge processing, and cloud AI work together to deliver actionable insights and automations for farmers.

### End-to-End Data Flow
1. **Satellite layer** ingests multispectral and weather-related remote data.
2. **Sensor network layer** captures hyperlocal soil, climate, and equipment telemetry.
3. **Edge computing layer** performs filtering, local inference, and rule-based controls on-farm.
4. **AI analysis layer** fuses historical + live data for predictions and recommendations.
5. **Farmer interface layer** provides alerts, maps, trends, and control actions via mobile/web.
6. **Feedback loop** records farmer actions and outcomes to continuously improve models.

### High-Level Logical Components
- Data ingestion services (satellite APIs, IoT broker ingest)
- Time-series & geospatial storage
- Feature engineering + model training pipelines
- Model serving (cloud + edge)
- Automation services (irrigation, alert engine)
- Farmer-facing application APIs
- Security, identity, and observability stack

---

## 2) Layered Design

## 2.1 Satellite Data Layer

### Purpose
Provide large-scale crop and environment visibility for field-level health and temporal trend detection.

### Inputs
- Sentinel-2 / Landsat multispectral imagery (10–30m)
- Optional commercial higher-resolution imagery
- Weather data (rainfall, temperature, evapotranspiration proxies)

### Processing
- Cloud masking and atmospheric correction
- Tile stitching and field boundary clipping
- Vegetation/water indices:
  - NDVI, EVI (crop vigor)
  - NDWI (water stress)
  - SAVI (soil-adjusted vegetation)
- Change detection across time windows (7/14/30 days)

### Outputs
- Per-plot health score
- Stress anomaly heatmaps
- Forecast features for yield and irrigation demand models

---

## 2.2 Sensor Network Layer

### Purpose
Capture high-frequency, local ground-truth conditions for precise decisions.

### On-Farm Sensors
- Soil moisture (multiple depths, e.g., 10cm/30cm)
- Soil temperature
- Soil EC (electrical conductivity)
- pH (periodic or continuous depending sensor type)
- Air temperature/humidity
- Rain gauge
- Wind speed/direction (optional)
- Leaf wetness (for disease risk models)
- Flow meter + pressure sensors (irrigation system)

### Connectivity
- **Field network**: LoRaWAN (long range, low power)
- **Gateway uplink**: 4G/5G/Ethernet/Wi-Fi
- **Message protocol**: MQTT with QoS and retry policies

### Outputs
- Time-series telemetry (1–15 min intervals)
- Device health data (battery, signal strength, uptime)

---

## 2.3 Edge Computing Layer

### Purpose
Ensure low-latency decisions and resilience when cloud connectivity is intermittent.

### Edge Functions
- Sensor data validation, smoothing, outlier filtering
- Local feature extraction (rolling averages, evapotranspiration approximations)
- On-device inference for:
  - irrigation triggers
  - anomaly flags
  - basic disease early warning (if camera available)
- Offline-first rule engine with fallback automations
- Local cache and delayed synchronization to cloud

### Control Outputs
- Valve on/off schedules
- Pump control recommendations/commands
- Emergency alerts (leak, extreme moisture deficit)

---

## 2.4 AI Analysis Layer

### Purpose
Fuse multimodal data into predictions and recommendations.

### Data Platform
- Time-series DB for IoT (e.g., TimescaleDB/InfluxDB)
- Object storage for imagery (e.g., S3-compatible)
- Geospatial store (PostGIS)
- Feature store for model reproducibility

### Core AI Services
1. **Crop health monitoring**
   - Combines vegetation indices + sensor data + weather
   - Produces per-zone health and stress ranking
2. **Soil moisture forecasting**
   - Predicts next 24–72h moisture trajectory
   - Supports proactive irrigation planning
3. **Irrigation optimization**
   - Recommends irrigation amount/timing by zone
   - Objective: maximize yield and water-use efficiency
4. **Disease risk detection**
   - Uses microclimate + leaf wetness + (optional) image model
   - Produces risk level and scouting priority maps
5. **Yield prediction**
   - Stage-wise estimation updated through season
   - Inputs include planting date, weather profile, growth trends

### MLOps
- Data quality checks and drift detection
- Scheduled retraining (seasonal/monthly)
- Model registry and versioned deployment
- A/B evaluation of recommendation strategies

---

## 2.5 Farmer Interface Layer

### Purpose
Convert model outputs into clear, localized, actionable guidance.

### User Experience
- Mobile-first dashboard (low bandwidth mode)
- Plot map with color-coded health and moisture
- Alert center:
  - irrigation needed
  - disease risk high
  - sensor offline
- Recommended actions with confidence score
- Manual override for automation decisions
- Local language support and voice notifications (optional)

### Interaction Types
- Read-only insights
- Approval-based automation (human-in-the-loop)
- Full automatic mode with guardrails and audit log

---

## 3) Working Prototype Design (One Farm)

### Farm Assumption
- 1 farm, ~20–50 acres
- 4 irrigation zones
- Mixed variability in soil moisture

### Prototype Objectives (MVP)
- Monitor crop health weekly from satellite data
- Track soil moisture in near-real-time
- Trigger or recommend irrigation actions
- Generate basic disease risk alerts

### Prototype Architecture (Practical)
- **Satellite ingest**: scheduled pipeline (daily/weekly)
- **Sensors**: 12–20 nodes across zones
- **Edge gateway**: one industrial SBC at farm office/pump room
- **Cloud backend**: API + time-series + model services
- **Farmer app**: web/PWA + SMS/WhatsApp alerts

---

## 4) Hardware Stack

### Field Devices
- Capacitive soil moisture probes (depth-based pairs)
- Soil temp + EC probes
- Micro weather station (temp/humidity/rain/wind)
- Leaf wetness sensors (disease-prone crops)
- Flow meters + pressure transducers on irrigation lines

### Compute and Network
- LoRaWAN sensor nodes (solar/battery)
- LoRaWAN gateway (8-channel or better)
- Edge compute unit (Jetson Orin Nano / Raspberry Pi 5 + TPU)
- Industrial relay/PLC interface for pump/valve actuation
- 4G router with fallback SIM

### Cloud/Server Stack
- Message broker (MQTT)
- Stream processing service
- Time-series database
- Geospatial services
- Model serving endpoints
- Notification service (SMS/push)

---

## 5) AI Models

### 5.1 Crop Health Monitoring
- **Model type**: Gradient boosting or temporal CNN on fused features
- **Inputs**: NDVI/EVI/NDWI time series, soil moisture, weather
- **Output**: health score (0–100), stress class (normal/watch/critical)

### 5.2 Soil Moisture Prediction
- **Model type**: LSTM/Temporal Fusion Transformer (or XGBoost baseline)
- **Inputs**: moisture history, weather forecast, irrigation logs, soil type
- **Output**: moisture trajectory by zone (24h/48h/72h)

### 5.3 Irrigation Optimization
- **Model type**: constrained optimization + rule-based safety guardrails
- **Inputs**: forecasted moisture deficit, crop stage, flow constraints, tariffs
- **Output**: start time, duration, expected water use

### 5.4 Disease Detection/Risk
- **Model type**:
  - tabular risk model (humidity + temperature + leaf wetness)
  - optional edge vision model (e.g., MobileNet/EfficientNet)
- **Output**: disease risk index and scouting recommendations

### 5.5 Yield Prediction
- **Model type**: ensemble regressor with stage-aware updates
- **Inputs**: historical yield, weather profile, health features, interventions
- **Output**: expected yield and uncertainty interval

### AI Deployment Strategy
- Start with interpretable baselines
- Add deep models where measurable lift exists
- Keep fallback rules active for safety-critical controls

---

## 6) Prototype Roadmap

## Phase 0: Planning (Weeks 1–2)
- Farm survey and zone mapping
- Sensor placement plan and connectivity test
- Define baseline agronomic KPIs (water usage, stress events)

## Phase 1: Infrastructure Setup (Weeks 3–5)
- Install sensors, gateway, and edge node
- Configure MQTT topics and ingestion pipeline
- Set up time-series and geospatial storage

## Phase 2: Data + Dashboard MVP (Weeks 6–8)
- Build farmer dashboard with live telemetry
- Integrate satellite index pipeline
- Enable alerting for threshold breaches

## Phase 3: AI MVP (Weeks 9–12)
- Train initial moisture forecast and health scoring models
- Deploy irrigation recommendation engine
- Implement disease risk scoring

## Phase 4: Automation Pilot (Weeks 13–16)
- Enable semi-automatic irrigation approvals
- Measure water savings and crop response
- Tune thresholds and recommendation confidence

## Phase 5: Evaluation + Scale Plan (Weeks 17–20)
- Compare against baseline season metrics
- Validate ROI and reliability
- Prepare multi-farm rollout architecture

---

## 7) Key Risks and Mitigations

1. **Sensor drift/failure**
   - Mitigation: calibration schedule, redundancy, auto health checks
2. **Connectivity instability**
   - Mitigation: edge buffering, store-and-forward sync, local control fallback
3. **Satellite cloud cover gaps**
   - Mitigation: temporal interpolation and multi-source imagery
4. **Model drift across seasons/crops**
   - Mitigation: drift monitoring + seasonal retraining
5. **Automation safety concerns**
   - Mitigation: hard limits, manual override, audit logging
6. **Farmer adoption challenges**
   - Mitigation: simple recommendations, local language UI, training support
7. **Data privacy and security**
   - Mitigation: encrypted transport, role-based access, signed device identity
8. **Cost overrun risk**
   - Mitigation: phased deployment, KPI-gated scaling decisions

---

## 8) Success Metrics for the One-Farm Prototype

- 10–25% reduction in irrigation water use
- Improved moisture stability within target bands
- Reduced stress-event response time
- Disease scouting efficiency improvement
- Measurable farmer action rate on recommendations
- Positive seasonal yield or quality uplift trend

