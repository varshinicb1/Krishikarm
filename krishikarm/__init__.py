"""
Krishikarm -- AI-powered crop distress prediction from satellite data.

Quick start::

    from krishikarm import Predictor

    p = Predictor()
    result = p.predict({
        "lat": 12.97, "lon": 77.59,
        "T2M": 32, "RH2M": 65, "PREC": 2.5,
        "state": "KA", "irrig": "borewell",
        "crops": ["rice"],
    })
    print(result["risk_label"])  # "Healthy"
"""

__version__ = "0.1.0"

from .model import KisanNetV3, RISK_LABELS, STATES, IRRIGATION, N_FEATURES
from .predict import Predictor
from .features import engineer_sample, to_tensors

__all__ = [
    "KisanNetV3",
    "Predictor",
    "engineer_sample",
    "to_tensors",
    "RISK_LABELS",
    "STATES",
    "IRRIGATION",
    "N_FEATURES",
]
