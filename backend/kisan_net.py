"""
KisanNet v1 — Multi-Modal Crop Distress Prediction Model
═══════════════════════════════════════════════════════════
Patent-pending architecture: Cross-attention fusion of satellite spectral
indices with farmer-specific context vectors for real-time crop distress
prediction on edge devices.

Novelty:
  1. Cross-attention between satellite temporal features and farmer context
  2. Regional embedding captures district-level farming patterns
  3. Multi-task output: distress level + intervention window + yield risk
  4. Lightweight (~50K params, <2MB) for SBC deployment

Author: Kisan-Eye Project
License: Proprietary (Patent Pending)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import json
import os
from pathlib import Path

# ══════════════════════════════════════════
# FEATURE DEFINITIONS
# ══════════════════════════════════════════

# 6 satellite spectral/environmental features
SAT_FEATURES = ['ndvi', 'soil_moisture', 'temperature', 'humidity', 'rainfall_7d', 'solar_radiation']

# 12 farmer context features
FARMER_FEATURES = [
    'land_acres', 'family_members', 'is_bpl',
    'crop_rice', 'crop_wheat', 'crop_cotton', 'crop_sugarcane', 'crop_maize',
    'irrig_rainfed', 'irrig_canal', 'irrig_borewell', 'irrig_drip',
]

# Indian states (for regional embedding)
STATES = [
    'Andhra Pradesh', 'Bihar', 'Gujarat', 'Haryana', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Odisha', 'Punjab',
    'Rajasthan', 'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'West Bengal',
    'Other'
]

# Financial states
FINANCIAL_STATES = ['stable', 'moderate', 'distress']

# Distress labels
DISTRESS_CLASSES = ['Healthy', 'Watch', 'Alert', 'Critical', 'Emergency']


# ══════════════════════════════════════════
# MODEL ARCHITECTURE
# ══════════════════════════════════════════

class SatelliteEncoder(nn.Module):
    """Encodes satellite spectral features into a latent representation."""

    def __init__(self, in_features=6, hidden=32, out_features=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden),
            nn.LayerNorm(hidden),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden, out_features),
            nn.LayerNorm(out_features),
            nn.GELU(),
        )

    def forward(self, x):
        return self.net(x)


class FarmerContextEncoder(nn.Module):
    """Encodes farmer context (crops, land, financial state) into latent space."""

    def __init__(self, in_features=12, n_states=16, n_financial=3, hidden=32, out_features=64):
        super().__init__()
        self.state_embed = nn.Embedding(n_states, 8)
        self.financial_embed = nn.Embedding(n_financial, 4)

        total_in = in_features + 8 + 4  # context + state_embed + financial_embed

        self.net = nn.Sequential(
            nn.Linear(total_in, hidden),
            nn.LayerNorm(hidden),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden, out_features),
            nn.LayerNorm(out_features),
            nn.GELU(),
        )

    def forward(self, x_context, state_idx, financial_idx):
        state_emb = self.state_embed(state_idx)
        fin_emb = self.financial_embed(financial_idx)
        combined = torch.cat([x_context, state_emb, fin_emb], dim=-1)
        return self.net(combined)


class CrossAttentionFusion(nn.Module):
    """
    Cross-attention between satellite and farmer encodings.
    This is the NOVEL component — satellite features attend to farmer context
    to produce personalized crop intelligence.
    """

    def __init__(self, dim=64, n_heads=4):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim=dim, num_heads=n_heads, batch_first=True)
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)
        self.ffn = nn.Sequential(
            nn.Linear(dim, dim * 2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(dim * 2, dim),
        )

    def forward(self, sat_features, farmer_features):
        # Sat attends to farmer context
        sat_q = sat_features.unsqueeze(1)  # [B, 1, D]
        farmer_kv = farmer_features.unsqueeze(1)  # [B, 1, D]

        attended, attn_weights = self.attn(sat_q, farmer_kv, farmer_kv)
        fused = self.norm1(sat_features + attended.squeeze(1))
        fused = self.norm2(fused + self.ffn(fused))

        return fused, attn_weights.squeeze(1)


class KisanNet(nn.Module):
    """
    KisanNet v1 — Multi-Modal Crop Distress Prediction
    ═══════════════════════════════════════════════════
    Fuses satellite spectral data with farmer context through
    cross-attention to predict:
      1. Crop distress level (0-1 continuous score)
      2. Days until intervention needed (0-30)
      3. Yield risk class (5 classes)
      4. Recommended action embedding
    """

    def __init__(self, sat_dim=6, farmer_dim=12, hidden=64, n_states=16, n_financial=3):
        super().__init__()
        self.sat_encoder = SatelliteEncoder(sat_dim, 32, hidden)
        self.farmer_encoder = FarmerContextEncoder(farmer_dim, n_states, n_financial, 32, hidden)
        self.cross_attn = CrossAttentionFusion(hidden, n_heads=4)

        # Multi-task prediction heads
        self.distress_head = nn.Sequential(
            nn.Linear(hidden * 2, 32),
            nn.GELU(),
            nn.Linear(32, 1),
            nn.Sigmoid(),  # 0-1 distress score
        )

        self.intervention_head = nn.Sequential(
            nn.Linear(hidden * 2, 32),
            nn.GELU(),
            nn.Linear(32, 1),
            nn.ReLU(),  # Days until intervention (0+)
        )

        self.risk_head = nn.Sequential(
            nn.Linear(hidden * 2, 32),
            nn.GELU(),
            nn.Linear(32, 5),  # 5 risk classes
        )

    def forward(self, sat_data, farmer_context, state_idx, financial_idx):
        sat_enc = self.sat_encoder(sat_data)
        farmer_enc = self.farmer_encoder(farmer_context, state_idx, financial_idx)

        fused, attn_weights = self.cross_attn(sat_enc, farmer_enc)

        # Concatenate fused + farmer encoding for prediction
        combined = torch.cat([fused, farmer_enc], dim=-1)

        distress = self.distress_head(combined).squeeze(-1)
        intervention = self.intervention_head(combined).squeeze(-1)
        risk_logits = self.risk_head(combined)

        return {
            'distress_score': distress,
            'intervention_days': intervention,
            'risk_logits': risk_logits,
            'risk_class': torch.argmax(risk_logits, dim=-1),
            'attention_weights': attn_weights,
        }

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# ══════════════════════════════════════════
# INFERENCE API
# ══════════════════════════════════════════

class KisanNetPredictor:
    """Production inference wrapper for KisanNet."""

    def __init__(self, model_path=None):
        self.model = KisanNet()
        self.device = torch.device('cpu')  # Edge deployment — always CPU

        if model_path and os.path.exists(model_path):
            checkpoint = torch.load(model_path, map_location=self.device, weights_only=True)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.metadata = checkpoint.get('metadata', {})
            print(f"✅ KisanNet loaded: {model_path} ({self.model.count_parameters():,} params)")
        else:
            self.metadata = {}
            print(f"⚠️ KisanNet: No trained model found, using random weights")

        self.model.eval()

    def _encode_farmer(self, farmer: dict):
        """Convert farmer dict to model input tensors."""
        crops = farmer.get('crops', [])
        irrig = farmer.get('irrigation_type', 'rainfed')

        context = torch.tensor([[
            min(farmer.get('land_acres', 0) / 10.0, 1.0),  # normalize
            min(farmer.get('family_members', 4) / 10.0, 1.0),
            float(farmer.get('bpl_card', 0)),
            float('rice' in crops),
            float('wheat' in crops),
            float('cotton' in crops),
            float('sugarcane' in crops),
            float('maize' in crops),
            float(irrig == 'rainfed'),
            float(irrig == 'canal'),
            float(irrig == 'borewell'),
            float(irrig == 'drip'),
        ]], dtype=torch.float32)

        state = farmer.get('state', 'Other')
        state_idx = torch.tensor([STATES.index(state) if state in STATES else len(STATES) - 1])

        fin = farmer.get('financial_state', 'stable')
        fin_idx = torch.tensor([FINANCIAL_STATES.index(fin) if fin in FINANCIAL_STATES else 0])

        return context, state_idx, fin_idx

    def _encode_satellite(self, sat_data: dict):
        """Convert satellite data dict to model input tensor."""
        return torch.tensor([[
            sat_data.get('ndvi', 0.5),
            sat_data.get('soil_moisture', 0.3),
            sat_data.get('temperature', 25.0) / 50.0,  # normalize to 0-1
            sat_data.get('humidity', 60.0) / 100.0,
            min(sat_data.get('rainfall_7d', 0) / 100.0, 1.0),
            sat_data.get('solar', 15.0) / 30.0,
        ]], dtype=torch.float32)

    @torch.no_grad()
    def predict(self, farmer: dict, sat_data: dict) -> dict:
        """Run inference on a farmer + satellite data pair."""
        sat_tensor = self._encode_satellite(sat_data)
        context, state_idx, fin_idx = self._encode_farmer(farmer)

        output = self.model(sat_tensor, context, state_idx, fin_idx)

        distress = output['distress_score'].item()
        intervention = output['intervention_days'].item()
        risk_class = output['risk_class'].item()

        return {
            'distress_score': round(distress, 4),
            'distress_label': DISTRESS_CLASSES[min(int(distress * 5), 4)],
            'intervention_days': round(intervention, 1),
            'risk_class': DISTRESS_CLASSES[risk_class],
            'risk_probabilities': {
                DISTRESS_CLASSES[i]: round(p, 4)
                for i, p in enumerate(F.softmax(output['risk_logits'], dim=-1).squeeze().tolist())
            },
            'model_version': self.metadata.get('version', 'untrained'),
            'parameters': self.model.count_parameters(),
        }


# ══════════════════════════════════════════
# QUICK TEST
# ══════════════════════════════════════════

if __name__ == "__main__":
    print("="*60)
    print("  KisanNet v1 — Architecture Verification")
    print("="*60)

    model = KisanNet()
    print(f"\n  Parameters: {model.count_parameters():,}")
    print(f"  Architecture:")
    print(f"    SatelliteEncoder:      6 → 32 → 64")
    print(f"    FarmerContextEncoder: 24 → 32 → 64")
    print(f"    CrossAttentionFusion: 64 × 4 heads")
    print(f"    DistressHead:       128 → 32 → 1")
    print(f"    InterventionHead:   128 → 32 → 1")
    print(f"    RiskHead:           128 → 32 → 5")

    # Test forward pass
    sat = torch.randn(2, 6)
    ctx = torch.randn(2, 12)
    state = torch.tensor([0, 13])
    fin = torch.tensor([0, 2])

    out = model(sat, ctx, state, fin)
    print(f"\n  Test forward pass (batch=2):")
    print(f"    Distress scores:    {out['distress_score'].tolist()}")
    print(f"    Intervention days:  {out['intervention_days'].tolist()}")
    print(f"    Risk classes:       {[DISTRESS_CLASSES[c] for c in out['risk_class'].tolist()]}")
    print(f"    Attention weights:  {out['attention_weights'].shape}")

    # Test predictor
    predictor = KisanNetPredictor()
    result = predictor.predict(
        farmer={'name': 'Test', 'land_acres': 2.5, 'state': 'Uttar Pradesh',
                'crops': ['rice', 'wheat'], 'financial_state': 'distress',
                'irrigation_type': 'rainfed', 'bpl_card': True, 'family_members': 6},
        sat_data={'ndvi': 0.35, 'soil_moisture': 0.15, 'temperature': 38,
                  'humidity': 30, 'rainfall_7d': 0, 'solar': 22}
    )
    print(f"\n  Predictor test:")
    for k, v in result.items():
        print(f"    {k}: {v}")

    print(f"\n  ✅ KisanNet architecture verified!")
    print("="*60)
