"""
Feature engineering for KisanNet v3.

Converts raw satellite / weather observations into the 42-dimensional
feature vector and 9-dimensional context vector expected by the model.
"""

import math
import numpy as np
import torch

from .model import STATES, IRRIGATION, N_FEATURES


def safe(value, default=0, scale=1.0):
    """Return a normalised float, falling back to *default* on None / NaN / -999."""
    if value is None or value == -999:
        return default
    if isinstance(value, float) and math.isnan(value):
        return default
    return float(value) / scale


def engineer_sample(s: dict) -> dict:
    """Add derived fields (VPD, TRANGE, NDVI_PROXY, GDD, DISTRESS, etc.) to a
    single raw observation dict *s*.  Mutates and returns *s*."""
    t = safe(s.get("T2M"), 25)
    td = safe(s.get("TDEW"), 15)
    rh = safe(s.get("RH2M"), 50)
    prec = safe(s.get("PREC"), 0)

    # Vapor pressure deficit
    es = 0.6108 * math.exp(17.27 * t / (t + 237.3)) if t > -40 else 0.6
    ea = 0.6108 * math.exp(17.27 * td / (td + 237.3)) if td > -40 else 0.3
    s["VPD"] = max(es - ea, 0)

    tmax = safe(s.get("T2M_MAX"), t + 5)
    tmin = safe(s.get("T2M_MIN"), t - 5)
    s["TRANGE"] = tmax - tmin

    # NDVI proxy from available meteorological data
    solar = safe(s.get("SOLAR"), 15)
    mf = min(1.0, (prec * 7 + rh * 0.3) / 100)
    tf2 = 1.0 - abs(t - 25) / 25
    sf = min(solar / 25, 1.0)
    s["NDVI_PROXY"] = float(np.clip(0.2 + 0.6 * mf * max(tf2, 0) * sf, 0, 0.95))

    s["GDD"] = max(0, t - 10)

    # Distress label
    distress = 0.0
    if t > 38:
        distress += (t - 38) * 0.05
    if t > 42:
        distress += 0.15
    if t < 5:
        distress += (5 - t) * 0.04
    if prec < 1 and rh < 40:
        distress += 0.15
    if prec < 0.5 and s.get("i") == "rainfed":
        distress += 0.2
    if s["VPD"] > 2.0:
        distress += (s["VPD"] - 2) * 0.1
    if prec > 50:
        distress += (prec - 50) * 0.005
    if prec > 100:
        distress += 0.2
    if 0 < solar < 8:
        distress += (8 - solar) * 0.02
    w = safe(s.get("WIND"), 2)
    if w > 8:
        distress += (w - 8) * 0.03
    pm = safe(s.get("PM25"), 20)
    if pm > 100:
        distress += (pm - 100) * 0.001
    uv = safe(s.get("UV"), 5)
    if uv > 10:
        distress += (uv - 10) * 0.01

    s["DISTRESS"] = float(np.clip(distress, 0, 1))
    s["INTERVENTION"] = max(0, 30 * (1 - s["DISTRESS"]))
    d = s["DISTRESS"]
    s["RISK"] = 0 if d < 0.15 else 1 if d < 0.30 else 2 if d < 0.50 else 3 if d < 0.75 else 4
    return s


def to_tensors(s: dict):
    """Convert a single (already-engineered) observation dict into the four
    tensors required by ``KisanNetV3.forward``.

    Returns
    -------
    feat : Tensor (1, 42)
    ctx  : Tensor (1, 9)
    state_idx : Tensor (1,)
    irrig_idx : Tensor (1,)
    """
    feat = torch.tensor([[
        safe(s.get("NDVI_PROXY"), 0.4),
        safe(s.get("SM0"), 0.3),
        safe(s.get("SM1"), 0.25),
        safe(s.get("SM3"), 0.2),
        safe(s.get("ST0"), 25, 50),
        safe(s.get("ST6"), 22, 50),
        safe(s.get("T2M"), 25, 50),
        safe(s.get("T2M_MAX"), 30, 50),
        safe(s.get("T2M_MIN"), 20, 50),
        safe(s.get("TRANGE"), 10, 25),
        safe(s.get("RH2M"), 50, 100),
        min(safe(s.get("PREC"), 0) / 50, 1),
        safe(s.get("SOLAR"), 15, 30),
        safe(s.get("WIND"), 2, 15),
        safe(s.get("VPD"), 1, 5),
        safe(s.get("CLOUD"), 50, 100),
        safe(s.get("TDEW"), 15, 35),
        safe(s.get("PS"), 100, 110),
        safe(s.get("LW"), 300, 500),
        min(safe(s.get("ET0"), 4) / 10, 1),
        safe(s.get("RAD"), 15, 35),
        min(safe(s.get("WMAX"), 5) / 20, 1),
        safe(s.get("PM25"), 20, 200),
        safe(s.get("PM10"), 40, 300),
        safe(s.get("DUST"), 5, 50),
        safe(s.get("UV"), 5, 15),
        safe(s.get("AOD"), 0.2, 1),
        safe(s.get("soil_clay"), 25, 100),
        safe(s.get("soil_sand"), 50, 100),
        safe(s.get("soil_soc"), 10, 50),
        safe(s.get("soil_ph"), 6.5, 14),
        safe(s.get("elevation"), 200, 5000),
        safe(s.get("GDD"), 15, 35),
        safe(s.get("WCODE"), 0, 100),
        s.get("DOY_SIN", 0),
        s.get("DOY_COS", 0),
        s.get("MON_SIN", 0),
        s.get("MON_COS", 0),
        safe(s.get("lat"), 20, 35),
        safe(s.get("lon"), 80, 100),
        len(s.get("crops", [])) / 5.0,
        1.0 if any(c in s.get("crops", []) for c in ["rice", "wheat"]) else 0.0,
    ]], dtype=torch.float32)

    crops = s.get("crops", [])
    ctx = torch.tensor([[
        safe(s.get("lat"), 20, 35),
        safe(s.get("lon"), 80, 100),
        len(crops) / 5.0,
        1.0 if "rice" in crops else 0.0,
        1.0 if "wheat" in crops else 0.0,
        1.0 if "cotton" in crops else 0.0,
        1.0 if "sugarcane" in crops else 0.0,
        safe(s.get("soil_clay"), 25, 100),
        safe(s.get("elevation"), 200, 5000),
    ]], dtype=torch.float32)

    st = s.get("state", "Other")
    state_idx = torch.tensor([STATES.index(st) if st in STATES else len(STATES) - 1])
    ir = s.get("irrig", "rainfed")
    irrig_idx = torch.tensor([IRRIGATION.index(ir) if ir in IRRIGATION else 0])

    return feat, ctx, state_idx, irrig_idx
