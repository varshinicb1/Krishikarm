# KisanNet v3 -- Model Card

## Model Details

| Property | Value |
|----------|-------|
| **Name** | KisanNet v3 |
| **Type** | Cross-attention transformer |
| **Parameters** | 3.8M |
| **Framework** | PyTorch |
| **License** | MIT |
| **Version** | 0.1.0 |

## Architecture

KisanNet v3 is a multi-modal crop distress prediction network that fuses satellite/weather features with geospatial context through learned cross-attention.

- **Satellite encoder**: 3-layer MLP (42 -> 256) with LayerNorm, GELU, Dropout
- **Context encoder**: 3-layer MLP (45 -> 256) with state and irrigation embeddings
- **Cross-attention**: 4-layer, 8-head multi-head attention (query: satellite, key/value: context)
- **Prediction heads**: Distress score (sigmoid), intervention days (ReLU), risk class (5-way softmax)

## Training Data

- **Source**: 82,000+ real satellite observations
- **Coverage**: 127 Indian districts, multiple seasons
- **APIs**: NASA POWER, Open-Meteo, SoilGrids, Open-Elevation
- **Features**: 42 normalised satellite/weather features including NDVI proxy, soil moisture at 3 depths, VPD, GDD, PM2.5

## Performance

| Metric | Value |
|--------|-------|
| Test accuracy (5-class) | 96.8% |
| Inference latency (GPU) | < 5ms |
| Inference latency (CPU) | < 20ms |

## Risk Classes

| Class | Label | Distress Range |
|-------|-------|---------------|
| 0 | Healthy | < 0.15 |
| 1 | Watch | 0.15 - 0.30 |
| 2 | Moderate | 0.30 - 0.50 |
| 3 | Severe | 0.50 - 0.75 |
| 4 | Critical | >= 0.75 |

## Input Features (42 dimensions)

NDVI_PROXY, SM0, SM1, SM3, ST0, ST6, T2M, T2M_MAX, T2M_MIN, TRANGE, RH2M, PREC, SOLAR, WIND, VPD, CLOUD, TDEW, PS, LW, ET0, RAD, WMAX, PM25, PM10, UV, CO, NO2, SO2, O3, AOD, CAPE, CIN, SWE, SD, ALBEDO, LST_DAY, LST_NIGHT, LAI, FPAR, GPP, SM_ROOT, ET_ACTUAL

## Context Vector (9 dimensions)

Latitude, longitude, crop flags (rice, wheat, cotton, sugarcane, millet), soil type, elevation

## Usage

```python
from krishikarm import Predictor

predictor = Predictor()  # auto-selects GPU if available
result = predictor.predict({
    "lat": 12.97, "lon": 77.59,
    "T2M": 32, "RH2M": 65, "PREC": 2.5,
    "SOLAR": 18, "WIND": 3.2,
    "state": "KA", "irrig": "borewell",
    "crops": ["rice"],
})
print(result["distress_score"])   # 0.39
print(result["risk_label"])       # "Critical"
print(result["intervention_days"])# 18.3
```

## Download

- **PyPI**: `pip install krishikarm` (weights bundled)
- **GitHub Release**: Download `kisan_net_v3.pth` from the Releases page
- **Direct path**: `krishikarm/weights/kisan_net_v3.pth` in this repository

## Citation

```bibtex
@software{krishikarm2026,
  title={Krishikarm: AI Crop Distress Prediction from Satellite Data},
  author={varshinicb1},
  year={2026},
  url={https://github.com/varshinicb1/Krishikarm}
}
```

## Limitations

- Trained primarily on Indian agricultural data; accuracy may vary for other geographies
- Relies on derived features (NDVI proxy, VPD) rather than raw satellite imagery
- Weather/soil features should be recent (within 24-48 hours) for best accuracy
- Model assumes standard crop cycles; may not account for unusual farming practices
