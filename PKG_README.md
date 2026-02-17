# Krishikarm

**Crop distress prediction from satellite and weather data.**

Krishikarm uses KisanNet v3, a cross-attention transformer trained on 82,000+ real
satellite observations across 127 Indian districts, to predict crop health risk
in real time.

## Installation

```bash
pip install krishikarm
```

## Quick Start

```python
from krishikarm import Predictor

predictor = Predictor()

result = predictor.predict({
    "lat": 12.97,
    "lon": 77.59,
    "T2M": 32,
    "RH2M": 65,
    "PREC": 2.5,
    "SOLAR": 18,
    "WIND": 3,
    "state": "KA",
    "irrig": "borewell",
    "crops": ["rice"],
})

print(result)
# {
#     "distress_score": 0.12,
#     "intervention_days": 26.4,
#     "risk_class": 0,
#     "risk_label": "Healthy"
# }
```

## Model Architecture

KisanNet v3 is a cross-attention transformer with:

- **42 input features** derived from weather, soil, atmosphere, and location data
- **State and irrigation embeddings** for regional context
- **4-layer, 8-head cross-attention** fusion between satellite and context encoders
- **Three prediction heads**: distress score (0-1), intervention window (days), risk class (5 levels)
- **96.8% accuracy** on held-out test data

### Input Features

| Source       | Features                                                         |
|--------------|------------------------------------------------------------------|
| Weather      | Temperature, humidity, precipitation, wind, cloud cover, dew point |
| Solar        | Shortwave radiation, UV index, longwave radiation                |
| Soil         | Moisture (3 depths), temperature (2 depths), clay, sand, SOC, pH |
| Atmosphere   | PM2.5, PM10, dust, aerosol optical depth                         |
| Derived      | NDVI proxy, VPD, GDD, thermal range                              |
| Location     | Latitude, longitude, elevation, day-of-year encoding             |

### Risk Classes

| Class | Label     | Distress Range |
|-------|-----------|----------------|
| 0     | Healthy   | 0.00 - 0.15    |
| 1     | Watch     | 0.15 - 0.30    |
| 2     | Alert     | 0.30 - 0.50    |
| 3     | Critical  | 0.50 - 0.75    |
| 4     | Emergency | 0.75 - 1.00    |

## Data Sources

All training data was collected from free, open APIs:

- **NASA POWER** -- Solar radiation, temperature, humidity
- **Open-Meteo** -- Weather forecasts, soil moisture, UV, air quality
- **SoilGrids** -- Soil composition (clay, sand, SOC, pH)
- **Open-Elevation** -- Terrain altitude

No proprietary data or paid APIs were used.

## API Reference

### `Predictor`

```python
Predictor(weights_path=None, device=None)
```

- `weights_path` -- Path to a `.pth` checkpoint. Defaults to the bundled v3 weights.
- `device` -- `"cpu"` or `"cuda"`. Defaults to CUDA when available.

#### Methods

- `predict(observation: dict) -> dict` -- Run prediction on a single observation.
- `predict_batch(observations: list[dict]) -> list[dict]` -- Batch prediction.
- `info() -> dict` -- Return model metadata.

### `KisanNetV3`

The raw PyTorch model class, for advanced users who want to integrate the
architecture into their own training pipeline.

## Requirements

- Python >= 3.9
- PyTorch >= 2.0
- NumPy >= 1.24

## License

MIT
